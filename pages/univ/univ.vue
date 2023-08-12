<script setup>
import { ref, onMounted, computed, watch, inject } from 'vue';
import { getMustString } from '../../func';
import { provinces } from '../../const';
import Loading from '../../components/Loading.vue';

import LEchart from '@/uni_modules/lime-echart/components/l-echart/l-echart.vue';
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
	TitleComponent,
	TooltipComponent,
	GridComponent
} from 'echarts/components';
import { LabelLayout, UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
	TitleComponent,
	TooltipComponent,
	GridComponent,
	LineChart,
	LabelLayout,
	UniversalTransition,
	CanvasRenderer
]);

const chart1 = ref(null);
const chart2 = ref(null);

const mymajors = inject('majors');
const props = defineProps(['sid']);
const data = ref(null);
const loadingDialog = ref(null);
const tags = ref([]);

const rankByYear = ref(true);
const rankCurrentItem = ref(null);
const rankData = ref([]);
const rankDataFiltered = ref([]);
const rankSelectOptions = computed(() =>
	rankData.value.map((e) => ({ value: e[0], text: e[0] }))
);

const mustByYear = ref(true);
const mustCurrentItem = ref(null);
const mustData = ref([]);
const mustDataFiltered = ref([]);
const mustSelectOptions = computed(() =>
	mustData.value.map((e) => ({ value: e[0], text: e[0] }))
);

onMounted(() => {
	loadingDialog.value.open();

	uni.request({
		url: 'https://univ.techo.cool/api/get/univ',
		data: { sid: props.sid },
		success: (response) => {
			if (response.statusCode !== 200) return;
			data.value = response.data;

			let totalChartdata = data.value.ranks.reduce(
				(accumulator, currentObject) => {
					const { year, schedule } = currentObject[0];
					let counter = accumulator.find((item) => item[0] == year);
					if (!counter) {
						accumulator.push([year, schedule]);
					} else {
						counter[1] += schedule;
					}
					return accumulator;
				},
				[]
			);
			totalChartdata.sort((a, b) => a[0] - b[0]);
			let totalChartoption = {
				title: {
					left: 'center',
					text: '历年计划数'
				},
				textStyle: {
					fontFamily: ['Inter', 'Noto Sans SC'],
					fontWeight: 'bold'
				},
				grid: {
					left: '1%',
					right: '1%',
					bottom: '1%',
					containLabel: true
				},
				tooltip: {
					trigger: 'axis'
				},
				xAxis: {
					type: 'category'
				},
				yAxis: {
					type: 'value'
				},
				series: [
					{
						data: totalChartdata,
						name: '计划数',
						type: 'line',
						smooth: true,
						color: '#0075ff'
					}
				]
			};

			let rankChartdata = data.value.ranks.reduce(
				(accumulator, currentObject) => {
					const { year, rank } = currentObject[0];
					let counter = accumulator.find((item) => item[0] == year);
					if (!counter) {
						accumulator.push([year, rank]);
					} else {
						counter[1] = Math.max(rank, counter[1]);
					}
					return accumulator;
				},
				[]
			);
			rankChartdata.sort((a, b) => a[0] - b[0]);
			let rankChartoption = {
				title: {
					left: 'center',
					text: '历年(最高)位次号'
				},
				grid: {
					left: '1%',
					right: '1%',
					bottom: '1%',
					containLabel: true
				},
				tooltip: {
					trigger: 'axis'
				},
				xAxis: {
					type: 'category'
				},
				yAxis: {
					type: 'value'
				},
				series: [
					{
						data: rankChartdata,
						name: '位次号',
						type: 'line',
						smooth: true,
						color: '#0075ff'
					}
				]
			};

			chart1.value.init(echarts, (chart) => {
				chart.setOption(rankChartoption);
			});

			chart2.value.init(echarts, (chart) => {
				chart.setOption(totalChartoption);
			});

			watch(
				rankByYear,
				(val) => {
					rankData.value = Array.from(
						data.value.ranks.reduce(
							(accumulator, currentObject) => {
								let tag;
								if (val) tag = currentObject[0].year;
								else tag = currentObject[1].mname;
								if (!accumulator.has(tag)) {
									accumulator.set(tag, []);
								}
								accumulator.get(tag).push(currentObject);
								return accumulator;
							},
							new Map()
						)
					);
					rankData.value.sort((a, b) => b[0] - a[0]);
					rankCurrentItem.value = rankData.value[0][0];
				},
				{ immediate: true }
			);
			watch(
				rankCurrentItem,
				(val) => {
					let rank_data = rankData.value.find(
						(item) => item[0] == val
					)[1];
					if (rankByYear.value)
						rank_data.sort((a, b) => a[0].rank - b[0].rank);
					else rank_data.sort((a, b) => a[0].year - b[0].year);
					rankDataFiltered.value = rank_data;
				},
				{ immediate: true }
			);

			watch(
				mustByYear,
				(val) => {
					mustData.value = Array.from(
						data.value.musts.reduce(
							(accumulator, currentObject) => {
								let tag;
								if (val) tag = currentObject.year;
								else tag = currentObject.mname;
								if (!accumulator.has(tag)) {
									accumulator.set(tag, []);
								}
								accumulator.get(tag).push(currentObject);
								return accumulator;
							},
							new Map()
						)
					);
					mustData.value.sort((a, b) => b[0] - a[0]);
					mustCurrentItem.value = mustData.value[0][0];
				},
				{ immediate: true }
			);
			watch(
				mustCurrentItem,
				(val) => {
					let must_data = mustData.value.find(
						(item) => item[0] == val
					)[1];
					if (mustByYear.value)
						must_data.sort((a, b) => a.must - b.must);
					else must_data.sort((a, b) => a.year - b.year);
					mustDataFiltered.value = must_data;
				},
				{ immediate: true }
			);

			uni.request({
				url: 'https://univ.techo.cool/api/list/tags',
				success: (res) => {
					tags.value = data.value.utags.map(
						(item) => res.data.find((e) => e.tid == item).tname
					);
					loadingDialog.value.close();
				}
			});
		}
	});
});
</script>

<template>
	<Loading ref="loadingDialog" />
	<div class="main-content" v-show="data">
		<div v-if="data">
			<div class="p-10 flex justify-between items-center">
				<div class="majorInfo">
					<div class="text-bold text-2xl">{{ data.uname }}</div>
					<div style="color: #0891b2">
						{{ provinces[data.province] }}
					</div>
				</div>
				<div>
					<button open-type="share" size="mini" type="info">
						分享
					</button>
				</div>
			</div>
			<div class="px-10 mb-10 flex flex-wrap gap-4">
				<uni-tag v-for="tag in tags" :text="tag" type="info"></uni-tag>
			</div>
			<div class="mb-30 table-c">
				<uni-section title="历年投档数据" type="line">
					<div class="mb-10">
						<uni-data-select
							:clear="false"
							:localdata="rankSelectOptions"
							v-model="rankCurrentItem"
						></uni-data-select>
					</div>
					<uni-table border stripe>
						<uni-tr>
							<uni-th>
								<span>位次号</span>
							</uni-th>
							<uni-th>
								<span>专业</span>
							</uni-th>
							<uni-th>
								<span>分数线</span>
							</uni-th>
							<uni-th>
								<span>计划数</span>
							</uni-th>
							<uni-th>
								<span>收藏</span>
							</uni-th>
						</uni-tr>
						<uni-tr v-for="item in rankDataFiltered">
							<uni-td>{{ item[0].rank }}</uni-td>
							<uni-td>
								<navigator
									style="color: #0891b2"
									:url="
										'/pages/major/major?mid=' + item[1].mid
									"
								>
									<span class="whitespace-nowrap">
										{{ item[1].mname }}
									</span>
								</navigator>
							</uni-td>
							<uni-td>{{ item[0].score }}</uni-td>
							<uni-td>{{ item[0].schedule }}</uni-td>
							<uni-td>
								<button
									@click="() => mymajors.remove(item[0].mid)"
									class="myButton"
									type="info"
									v-if="mymajors.has(item[0].mid)"
								>
									收藏
								</button>
								<button
									@click="() => mymajors.add(item[0].mid)"
									class="myButton"
									v-else
								>
									收藏
								</button>
							</uni-td>
						</uni-tr>
					</uni-table>
				</uni-section>
			</div>
			<div class="mb-30">
				<uni-section title="必选科目要求" type="line">
					<div class="mb-10">
						<uni-data-select
							:clear="false"
							:localdata="mustSelectOptions"
							v-model="mustCurrentItem"
						></uni-data-select>
					</div>
					<uni-table border stripe>
						<uni-tr>
							<uni-th>专业</uni-th>
							<uni-th>必选科目</uni-th>
							<uni-th width="400">包含专业</uni-th>
						</uni-tr>
						<uni-tr v-for="item in mustDataFiltered">
							<uni-td>
								<span class="whitespace-nowrap">
									{{ item.mname }}
								</span>
							</uni-td>
							<uni-td>
								<span class="whitespace-nowrap">
									{{ getMustString(item.must) }}
								</span>
							</uni-td>
							<uni-td>
								<span class="whitespace-nowrap">
									{{ item.include }}
								</span>
							</uni-td>
						</uni-tr>
					</uni-table>
				</uni-section>
			</div>
		</div>
		<div style="height: 200px; width: 90%; margin: 1rem auto">
			<l-echart ref="chart1"></l-echart>
		</div>
		<div style="height: 200px; width: 90%; margin: 2rem auto">
			<l-echart ref="chart2"></l-echart>
		</div>
	</div>
	<div style="height: 1px"></div>
</template>

<style>
.table-c >>> .uni-table-td {
	padding: 5px;
}

.myButton {
	line-height: 1.4;
	font-size: 14px;
	padding: 4px 0;
}

.majorInfo {
	max-width: 70%;
}

page {
	background-color: #ebebeb;
}
</style>
