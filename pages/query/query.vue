<script setup>
import { provinces, majors } from '../../const';
import {
	getMustString,
	fixInteger,
	filterEmptyObject,
	findMaxValue
} from '../../func';
import { onMounted, ref, reactive, watch, inject, unref } from 'vue';
import { onShow } from '@dcloudio/uni-app';
import Loading from '../../components/Loading.vue';

const tags = ref([]);
const rank_years = ref([]);
const must_years = ref([]);
const mymajors = inject('majors');
const data = reactive({ total: 0, list: [] });
const loading = ref(true);
const last = ref(null);
const s = inject('s');
const page = ref(1);

var loaded = false;

const info = reactive({
	rank: null,
	year: 0,
	school: '',
	major: s,
	rank_range: null,
	utags: '',
	province: [],
	utags: [],
	nutags: [],
	mymust: [],
	standard: 0,
	accordation: 0
});

const inputDialog = ref(null);
const score = reactive({ year: info.year, score: 600 });

const infoDialog = ref(null);
const optionPop = ref(null);
const loadingDialog = ref(null);

uni.request({
	url: 'https://univ.techo.cool/api/list/tags',
	success: (response) => {
		tags.value = response.data.map((item) => ({
			text: item.tname,
			value: item.tid
		}));
	}
});

Promise.all([
	new Promise((resolve) => {
		uni.request({
			url: 'https://univ.techo.cool/api/list/ranks',
			success: (response) => {
				rank_years.value = response.data.map((item) => ({
					text: item,
					value: item
				}));
				if (!info.year)
					score.year = info.year = Math.max(...response.data);
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
				if (!info.standard) {
					let current = new Date().getFullYear();
					let currentMonth = new Date().getMonth();
					if (currentMonth >= 7) current += 1;
					info.standard = findMaxValue(response.data, current);
				}
				resolve();
			}
		});
	})
]).then(() => {
	loaded = true;
	goQuery();
});

onShow(() => {
	if (last.value !== s.value) goQuery();
});

const goQuery = () => {
	if (!loaded) return;
	loading.value = true;
	last.value = unref(s);
	info.page = page.value;
	if (!info.rank) info.rank = null;
	if (!info.rank_range) info.rank_range = null;
	uni.request({
		url: 'https://univ.techo.cool/api/query',
		method: 'POST',
		data: info
	}).then((response) => {
		data.total = response.data.total;
		if (data.total <= (page.value - 1) * 50) {
			page.value = 1;
			goQuery();
		}
		data.list = response.data.result;
		loading.value = false;
	});
};

const province_option = Object.keys(provinces)
	.slice(1)
	.map((item) => ({
		text: provinces[item],
		value: item
	}));

const must_options = majors.slice(1).map((item, index) => ({
	text: item,
	value: index + 1
}));

const fetchRank = () => {
	uni.request({
		url: 'https://univ.techo.cool/api/get/score',
		data: { score: score.score, year: score.year }
	}).then((response) => {
		if (response.data) {
			info.rank = response.data.rank;
			inputDialog.value.close();
		}
	});
};

const agree = () => {
	uni.setStorageSync('agreement', true);
	infoDialog.value.close();
};
const disagree = () => {
	uni.redirectTo({
		url: '/pages/index/index'
	});
};

onMounted(() => {
	loadingDialog.value.open();
	if (uni.getStorageSync('agreement') !== true) infoDialog.value.open();
});

watch(loading, (val) => {
	if (val) loadingDialog.value.open();
	else setTimeout(loadingDialog.value.close, 300);
});

const gotoMajor = (mid) => {
	uni.navigateTo({
		url: '/pages/major/major?mid=' + mid
	});
};
</script>

<template>
	<uni-popup ref="infoDialog" type="dialog">
		<uni-popup-dialog
			type="info"
			cancelText="关闭"
			confirmText="同意"
			title="免责声明"
			content="本页面提供数据来自政府教育考试机构。
			系统已经采取最佳可行算法自动处理相关数据，但仍可能存在必选科目匹配错误等信息有误情况。
			本系统仅供辅助查询，请您以相关学校以及教育考试机构官方数据为准。
			网站运营者不承担有关数据正确性的个别及连带责任。"
			@confirm="agree"
			@close="disagree"
		></uni-popup-dialog>
	</uni-popup>
	<uni-popup
		type="right"
		ref="optionPop"
		@maskClick="goQuery"
		background-color="#fafafa"
	>
		<scroll-view class="scrollView" :scroll-y="true">
			<div class="dialogContent">
				<uni-section title="位次号" type="line">
					<div class="flex items-center">
						<uni-easyinput type="number" v-model="info.rank" />
						<div class="ml-10">
							<button
								@click="() => inputDialog.open()"
								class="button"
								size="mini"
								type="info"
							>
								转换
							</button>
						</div>
					</div>
				</uni-section>
				<uni-section title="区间" type="line">
					<uni-easyinput type="number" v-model="info.rank_range" />
				</uni-section>
				<uni-section title="选考科目" type="line">
					<uni-data-checkbox
						multiple
						max="3"
						v-model="info.mymust"
						:localdata="must_options"
					></uni-data-checkbox>
				</uni-section>
				<uni-section title="一致优先" type="line">
					<uni-data-checkbox
						:localdata="[
							{ text: '是', value: 1 },
							{ text: '否', value: 0 }
						]"
						v-model="info.accordation"
					/>
				</uni-section>
				<uni-section title="选考标准" type="line">
					<uni-data-select
						v-model="info.standard"
						:clear="false"
						:localdata="must_years"
					></uni-data-select>
				</uni-section>
				<uni-section title="投档数据" :clear="false" type="line">
					<uni-data-select
						v-model="info.year"
						:clear="false"
						:localdata="rank_years"
					></uni-data-select>
				</uni-section>
				<uni-section title="省份" type="line">
					<uni-data-checkbox
						multiple
						v-model="info.province"
						:localdata="province_option"
					></uni-data-checkbox>
				</uni-section>
				<uni-section title="标签" type="line">
					<uni-data-checkbox
						multiple
						v-model="info.utags"
						:localdata="tags"
					></uni-data-checkbox>
				</uni-section>
			</div>
		</scroll-view>
	</uni-popup>
	<uni-popup ref="inputDialog" background-color="#fafafa">
		<div class="py-30 px-40">
			<span class="text-bold text-xl mt-10">分数转换</span>
			<uni-section title="年份" type="line">
				<uni-data-select
					v-model="score.year"
					:clear="false"
					:localdata="rank_years"
				></uni-data-select>
			</uni-section>
			<uni-section title="分数" type="line">
				<uni-easyinput type="number" v-model="score.score" />
			</uni-section>
			<div class="mt-20 flex justify-center">
				<button
					class="button"
					size="mini"
					type="info"
					@click="fetchRank"
				>
					确认
				</button>
			</div>
		</div>
	</uni-popup>
	<Loading ref="loadingDialog" />
	<div class="mx-8">
		<div class="flex gap-10 mx-10">
			<uni-section class="half" title="学校" type="line">
				<uni-easyinput v-model="info.school" />
			</uni-section>
			<uni-section class="half" title="专业" type="line">
				<uni-easyinput v-model="info.major" />
			</uni-section>
		</div>
		<div class="mt-10 flex justify-center">
			<div class="flex gap-10">
				<button
					@click="optionPop.open()"
					class="button"
					size="mini"
					type="default"
				>
					更多选项
				</button>
				<button @click="goQuery" class="button" size="mini" type="info">
					查找
				</button>
			</div>
		</div>
	</div>

	<div class="mt-10">
		<div class="mx-20 my-10">
			<span>共计找到了</span>
			<span>{{ data.total }}</span>
			<span>个专业。</span>
		</div>
		<div class="px-20 pb-5">
			<uni-pagination
				show-icon="true"
				:total="data.total"
				:page-size="50"
				v-model="page"
				v-if="data.total"
				@change="goQuery"
			></uni-pagination>
		</div>
		<uni-list v-if="data.total">
			<uni-list-item
				:to="'/pages/major/major?mid=' + item[0].mid"
				:clickable="true"
				direction="column"
				v-for="item in data.list"
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
								@click.stop="mymajors.remove(item[0].mid)"
								size="mini"
								type="info"
								v-if="mymajors.has(item[0].mid)"
							>
								<span class="whitespace-nowrap">收藏</span>
							</button>
							<button
								@click.stop="mymajors.add(item[0].mid)"
								size="mini"
								type="default"
								v-else
							>
								<span class="whitespace-nowrap">收藏</span>
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
		<div class="px-20 py-5">
			<uni-pagination
				show-icon="true"
				:total="data.total"
				:page-size="50"
				v-model="page"
				v-if="data.total"
				@change="goQuery"
			></uni-pagination>
		</div>
	</div>
</template>

<style>
.half {
	width: 50%;
}

.dialogContent {
	width: 60vw;
	padding: 1rem;
}

.scrollView {
	height: calc(100vh);
}
</style>
