<script setup>
import { ref, onMounted, reactive, watch, readonly, unref, inject } from 'vue';
import {
	findMaxValue,
	getMustString,
	isSubArray,
	base64toBlob
} from '../../func';
import { onShow } from '@dcloudio/uni-app';
import Loading from '../../components/Loading.vue';
import Empty from '../../components/Empty.vue';

import LEchart from '@/uni_modules/lime-echart/components/l-echart/l-echart.vue';
import * as echarts from 'echarts/core';
import { TitleComponent, SingleAxisComponent } from 'echarts/components';
import { ScatterChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
	TitleComponent,
	SingleAxisComponent,
	ScatterChart,
	CanvasRenderer,
	UniversalTransition
]);

const info = reactive({ year: null, standard: null });
const majors = inject('majors');
const last = ref([]);
const loading = ref(false);
const data = ref([]);
const loadingDialog = ref(null);
const alertDialog = ref(null);
const chart1 = ref(null);
const rank_years = ref([]);
const must_years = ref([]);

Promise.all([
	new Promise((resolve) => {
		uni.request({
			url: 'https://univ.techo.cool/api/list/ranks',
			success: (response) => {
				rank_years.value = response.data.map((item) => ({
					text: item,
					value: item
				}));
				info.year = Math.max(...response.data);
				resolve();
			}
		});
	}),
	new Promise((resolve) => {
		uni.request({
			url: 'https://univ.techo.cool/api/list/musts',
			success: (response) => {
				must_years.value = response.data.map((item) => ({
					text: item,
					value: item
				}));
				let current = new Date().getFullYear();
				info.standard = findMaxValue(response.data, current);
				resolve();
			}
		});
	})
]).then(() => {
	watch(data, renderTable);
	goQuery();
	watch(info, goQuery);
});

onShow(() => {
	if (!majors.get().every((e) => last.value.includes(e))) {
		goQuery();
	} else {
		data.value = data.value.filter((item) =>
			majors.get().includes(item[0].mid)
		);
		renderTable();
	}
});

const goQuery = () => {
	if (!majors.get().length || !info.year || !info.standard) return;
	loading.value = true;
	uni.request({
		url: 'https://univ.techo.cool/api/get/majors',
		method: 'POST',
		data: { ...info, majors: majors.get() },
		success: (response) => {
			last.value = [...majors.get()];
			data.value = response.data.result;
			loading.value = false;
		}
	});
};

const renderTable = () => {
	let options = {
		singleAxis: {
			top: 'middle',
			height: '0',
			type: 'value',
			boundaryGap: false
		},
		series: {
			coordinateSystem: 'singleAxis',
			type: 'scatter',
			data: data.value.map((item) => [item[2].rank, item[0].mname]),
			color: '#0075ff'
		}
	};

	chart1.value.init(echarts, (chart) => {
		chart.setOption(options);
	});
};

const removeItem = (mid) => {
	majors.remove(mid);
	data.value = data.value.filter((item) => item[0].mid != mid);
};

const cleanItem = () => {
	majors.clean();
	data.value = [];
};

watch(loading, (val) => {
	if (val) loadingDialog.value.open();
	else setTimeout(loadingDialog.value.close, 300);
});

const downloadTable = () => {
	loading.value = true;
	uni.request({
		url: 'https://univ.techo.cool/api/get/table',
		method: 'POST',
		data: { ...info, majors: majors.get() },
		success: (response) => {
			//#ifdef MP-WEIXIN
			const fileManager = uni.getFileSystemManager();
			let fileName =
				wx.env.USER_DATA_PATH +
				'/MyUNIV_' +
				new Date().getTime() +
				'.xlsx';
			fileManager.writeFile({
				filePath: fileName,
				data: response.data.file,
				encoding: 'base64',
				success: () => {
					loading.value = false;
					uni.openDocument({
						filePath: fileName,
						fileType: 'xlsx'
					});
				}
			});
			//#endif
			//#ifdef APP
			let blob = base64toBlob(response.data.file);
			let url = URL.createObjectURL(blob);
			uni.downloadFile({
				url: url,
				success: (res) => {
					loading.value = false;
					uni.openDocument({
						filePath: res.tempFilePath,
						fileType: 'xlsx'
					});
				}
			});
			//#endif
		}
	});
};
</script>

<template>
	<Loading ref="loadingDialog" />
	<uni-popup ref="alertDialog" type="dialog">
		<uni-popup-dialog
			type="warn"
			cancelText="取消"
			confirmText="好的"
			title="确认清空"
			content="确认要清空收藏？操作不可撤销"
			@confirm="cleanItem"
		></uni-popup-dialog>
	</uni-popup>
	<div class="mx-8">
		<div class="flex justify-center gap-25 mx-auto">
			<uni-section title="选考标准" type="line">
				<uni-data-select
					v-model="info.standard"
					:clear="false"
					:localdata="must_years"
				></uni-data-select>
			</uni-section>
			<uni-section title="投档数据" type="line">
				<uni-data-select
					v-model="info.year"
					:clear="false"
					:localdata="rank_years"
				></uni-data-select>
			</uni-section>
			<div class="flex flex-col justify-center mt-8">
				<!-- #ifdef APP || MP-WEIXIN -->
				<div>
					<button @click="downloadTable" size="mini" type="info">
						<span class="whitespace-nowrap">导出</span>
					</button>
				</div>
				<!-- #endif -->
				<div>
					<button
						@click="() => alertDialog.open()"
						size="mini"
						type="warn"
					>
						<span class="whitespace-nowrap">删除</span>
					</button>
				</div>
			</div>
		</div>
	</div>
	<div class="mt-10" v-if="majors.length">
		<div class="mx-10 text-center">
			<span>共计收藏了</span>
			<span>{{ majors.length }}</span>
			<span>个专业。</span>
		</div>
	</div>
	<div
		style="height: 50px; width: 90%; margin: 1rem auto"
		v-show="data.length"
	>
		<l-echart ref="chart1"></l-echart>
	</div>
	<div class="mb-20" v-if="data.length">
		<uni-list>
			<uni-list-item
				:to="'/pages/major/major?mid=' + item[0].mid"
				:clickable="true"
				direction="column"
				v-for="item in data"
			>
				<template #header>
					<div class="flex justify-between">
						<div>
							<div class="text-sm" style="color: #0891b2">
								{{ item[1].uname }}
							</div>
							<div class="text-lg mb-2">
								{{ item[0].mname }}
							</div>
						</div>
						<div class="ml-10">
							<button
								@click.stop="() => removeItem(item[0].mid)"
								size="mini"
								type="default"
							>
								<span class="whitespace-nowrap">删除</span>
							</button>
						</div>
					</div>
				</template>
				<template #body>
					<div class="flex gap-10">
						<div class="flex items-baseline gap-3">
							<span class="text-bold text-base">
								{{ item[2].score }}
							</span>
							<span class="text-sm">分</span>
						</div>
						<div class="flex items-baseline gap-3">
							<span class="text-bold text-base">
								{{ item[2].rank }}
							</span>
							<span class="text-sm">名</span>
						</div>
						<div class="flex items-baseline gap-3">
							<span class="text-bold text-base">
								{{ item[2].schedule }}
							</span>
							<span class="text-sm">计划</span>
						</div>
					</div>
				</template>
				<template #footer>
					<span class="text-sm" style="color: #4c1d95">
						{{ getMustString(item[3].must) }}
					</span>
				</template>
			</uni-list-item>
		</uni-list>
	</div>
	<Empty v-else />
</template>
