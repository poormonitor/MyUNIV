<script setup>
import { inject, reactive, ref, watch } from 'vue';
import { majors } from '../const';
import GetRank from './GetRank.vue';

const infos = inject('infos');
const props = defineProps(['year', 'yearOptions']);
const emits = defineEmits(['finish']);
const show = ref(false);
const getRank = ref(null);
const inputDialog = ref(null);

const infoSet = reactive({
	rank: infos.getRank(),
	must: infos.getMust(),
	disabled: infos.getDisabled()
});

const must_options = majors.slice(1).map((item, index) => ({
	text: item,
	value: index + 1
}));

const setRank = (rank) => {
	infoSet.rank = rank;
};

const open = () => {
	infoSet.rank = infos.getRank();
	infoSet.must = infos.getMust();
	infoSet.disabled = infos.getDisabled();
	inputDialog.value.open();
};

const submitRequest = () => {
	infos.setRank(infoSet.rank);
	infoSet.must.sort((a, b) => a - b);
	infos.setMust(infoSet.must);
	infos.setDisabled(infoSet.disabled);
	inputDialog.value.close();
	emits('finish', infoSet.rank, infoSet.must);
};

defineExpose({
	open
});
</script>

<template>
	<uni-fab class="floatButton" @fabClick="open" horizontal="right" vertical="top" :pattern="{ icon: 'person', buttonColor: '#0284c799' }">
		<div class="mx-5" v-if="infos.isSetted()">
			<div v-if="infos.getRank()">{{ infos.getRank() }}</div>
			<div v-if="infos.getMust().length" class="whitespace-nowrap">
				{{ infos.getMust() }}
			</div>
		</div>
		<div class="mx-5" v-else>修改信息</div>
	</uni-fab>
	<uni-popup style="margin: 40px 0" ref="inputDialog" background-color="#fafafa">
		<div class="py-30 px-30">
			<div class="text-bold text-xl mb-10">修改个人信息</div>
			<div style="width: 70vw">
				<uni-section title="位次号" type="line">
					<div class="flex items-center">
						<uni-easyinput type="number" v-model="infoSet.rank" />
						<div class="ml-10">
							<button @click="() => getRank.open()" class="button" size="mini" type="info">转换</button>
						</div>
					</div>
				</uni-section>

				<uni-section title="选考科目" type="line">
					<uni-data-checkbox multiple max="3" v-model="infoSet.must" :localdata="must_options"></uni-data-checkbox>
				</uni-section>

				<uni-section title="不再提示" type="line">
					<uni-data-checkbox
						:localdata="[
							{ text: '是', value: 1 },
							{ text: '否', value: 0 }
						]"
						v-model="infoSet.disabled"
					/>
				</uni-section>
			</div>
			<div class="mt-20 flex justify-center">
				<button class="button" size="mini" type="info" @click="submitRequest">确认</button>
			</div>
		</div>
	</uni-popup>
	<GetRank ref="getRank" :year="props.year" :yearOptions="props.yearOptions" @rank="setRank" />
</template>
