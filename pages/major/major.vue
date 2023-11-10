<script setup>
import { ref, onMounted, inject } from 'vue';
import { getMustString } from '../../func';
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

const props = defineProps(['mid']);
const mymajors = inject('majors');
const data = ref(null);
const loadingDialog = ref(null);
const tags = ref([]);

const chart1 = ref(null);
const chart2 = ref(null);

const gotoUniv = (sid) => {
	uni.navigateTo({
		url: '/pages/univ/univ?sid=' + sid
	});
};

onMounted(() => {
	loadingDialog.value.open();

	uni.request({
		url: 'https://univ.techo.cool/api/get/major',
		data: { mid: props.mid },
		success: (response) => {
			if (response.statusCode !== 200) return;

			data.value = response.data;
			data.value.ranks.sort((a, b) => a.year - b.year);
			data.value.musts.sort((a, b) => a.year - b.year);
			tags.value = Array.from(
				data.value.musts.reduce((ac, ob) => {
					if (
						data.value.mname.includes(ob.mname) ||
						ob.mname.includes(data.value.mname)
					)
						ob.include.split('、').forEach((elem) => {
							if (elem) ac.add(elem);
						});
					return ac;
				}, new Set())
			);

			let totalChartdata = data.value.ranks.map((item) => [
				item.year,
				item.schedule
			]);
			totalChartdata.sort((a, b) => a[0] - b[0]);
			let totalChartoption = {
				title: {
					left: 'center',
					text: '历年计划数'
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

			let rankChartdata = data.value.ranks.map((item) => [
				item.year,
				item.rank
			]);
			rankChartdata.sort((a, b) => a[0] - b[0]);
			let rankChartoption = {
				title: {
					left: 'center',
					text: '历年位次号'
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

			loadingDialog.value.close();
		}
	});
});
</script>

<template>
	<Loading ref="loadingDialog" />
	<div class="main-content" v-show="data">
		<div v-if="data">
			<div class="p-10 pb-15">
				<div
					class="flex items-center mb-2"
					style="color: #0891b2"
					@click="gotoUniv(data.univ.sid)"
				>
					<span>{{ data.univ.uname }}</span>
					<image
						style="width: 12px; height: 12px"
						class="ml-3 mb-3"
						src="../../static/icons8-right-2-24.png"
					></image>
				</div>
				<div class="text-bold text-2xl">{{ data.mname }}</div>
				<div
					class="my-10 flex flex-wrap gap-4"
					style="line-height: 160%"
				>
					<uni-tag
						v-for="tag in tags"
						:text="tag"
						type="info"
					></uni-tag>
				</div>
				<div class="mt-12">
					<button
						@click.stop="() => mymajors.remove(data.mid)"
						size="mini"
						type="info"
						v-if="mymajors.has(data.mid)"
					>
						<span class="whitespace-nowrap">收藏</span>
					</button>
					<button
						@click.stop="() => mymajors.add(data.mid)"
						size="mini"
						type="default"
						v-else
					>
						<span class="whitespace-nowrap">收藏</span>
					</button>
					<button
						open-type="share"
						size="mini"
						class="ml-5"
						type="info"
					>
						分享
					</button>
				</div>
			</div>
			<div class="mb-10 table-c">
				<uni-section title="历年投档数据" type="line">
					<uni-table border stripe>
						<uni-tr>
							<uni-th>年份</uni-th>
							<uni-th>位次号</uni-th>
							<uni-th>分数线</uni-th>
							<uni-th>计划数</uni-th>
						</uni-tr>
						<uni-tr v-for="item in data.ranks">
							<uni-td>{{ item.year }}</uni-td>
							<uni-td>{{ item.rank }}</uni-td>
							<uni-td>{{ item.score }}</uni-td>
							<uni-td>{{ item.schedule }}</uni-td>
						</uni-tr>
					</uni-table>
				</uni-section>
			</div>
			<div class="mb-30">
				<uni-section title="必选科目要求" type="line">
					<uni-table border stripe>
						<uni-tr>
							<uni-th>年份</uni-th>
							<uni-th>专业</uni-th>
							<uni-th>必选科目</uni-th>
							<uni-th>包含专业</uni-th>
						</uni-tr>
						<uni-tr v-for="item in data.musts">
							<uni-td>{{ item.year }}</uni-td>
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
		<div style="height: 200px; width: 80%; margin: 2rem auto">
			<l-echart ref="chart2"></l-echart>
		</div>
	</div>
	<div style="height: 1px"></div>
</template>

<style>
.school {
	background-color: #ff7c00;
	color: #fff;
}
.table-c >>> .uni-table {
	min-width: auto !important;
}

page {
	background-color: #ebebeb;
}
</style>
