<script setup>
import { inject, onMounted, reactive, ref } from 'vue';
import Card from '../../components/Card.vue';

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

const option = {
	title: {
		text: '历年计划数',
		left: 'center'
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
			data: [],
			name: '计划数',
			type: 'line',
			smooth: true,
			color: '#383838'
		}
	]
};

const keyword = inject('s');
const chart = ref(null);

const search = () => {
	uni.switchTab({ url: '/pages/query/query' });
};

onMounted(() => {
	chart.value.init(echarts, (chart) => {
		chart.setOption(option);
		uni.request({
			url: 'https://univ.techo.cool/api/list/sums',
			success: (response) => {
				option.series[0].data = response.data;
				chart.setOption(option);
			}
		});
	});
});
</script>

<template>
	<div>
		<div class="title text-bold my-40 text-center">
			<div class="text-3xl mb-4">MyUNIV</div>
			<div class="text-xl font-bold">高考志愿填报决策分析系统</div>
		</div>
		<div class="mx-30">
			<uni-search-bar
				bgColor="#ffffff"
				placeholder="搜索专业"
				v-model="keyword"
				@confirm="search"
			></uni-search-bar>
		</div>
		<div style="height: 200px; width: 90%; margin: 2rem auto">
			<l-echart ref="chart"></l-echart>
		</div>
		<div class="flex flex-col px-40 pb-10">
			<Card title="易用">
				<template #content>
					前端逻辑清晰，操作提示直观，无需教学也可使用，极大的降低了学校专业查询成本。
				</template>
			</Card>
			<Card title="智能">
				<template #content>
					多种条件筛选符合要求的学校和专业，并可以根据相关要求自动筛选备选志愿供参考。
				</template>
			</Card>
			<Card title="全面">
				<template #content>
					历年数据一网打尽，不再需要多处访问、下载，一站式获得专业信息数据。
				</template>
			</Card>
		</div>
	</div>
</template>

<style>
.title {
	background-image: linear-gradient(
		to bottom left,
		#06b6d4,
		#0284c7,
		#1e40af
	);
	-webkit-background-clip: text;
	background-clip: text;
	color: transparent;
}
</style>
