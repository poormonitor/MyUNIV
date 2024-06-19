<script setup>
import { ref } from 'vue';
const props = defineProps(['yearOptions', 'year']);
const emits = defineEmits(['rank']);
const score = ref(600);
const year = ref(props.year);
const inputDialog = ref(null);

const fetchRank = () => {
	uni.request({
		url: 'https://univ.techo.cool/api/get/score',
		data: { score: score.value, year: year.value }
	}).then((response) => {
		if (response.data) {
			emits('rank', response.data.rank);
			inputDialog.value.close();
		}
	});
};

defineExpose({
	open: () => {
		year.value = props.year
		inputDialog.value.open();
	}
});
</script>

<template>
	<uni-popup ref="inputDialog" background-color="#fafafa">
		<div class="py-30 px-40">
			<span class="text-bold text-xl mt-10">分数转换</span>
			<uni-section title="年份" type="line">
				<uni-data-select v-model="year" :clear="false" :localdata="props.yearOptions"></uni-data-select>
			</uni-section>
			<uni-section title="分数" type="line">
				<uni-easyinput type="number" v-model="score" />
			</uni-section>
			<div class="mt-20 flex justify-center">
				<button class="button" size="mini" type="info" @click="fetchRank">确认</button>
			</div>
		</div>
	</uni-popup>
</template>
