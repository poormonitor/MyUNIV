<script setup>
import { ref } from 'vue';
const dialog = ref(null);
const open = () => dialog.value.open();
const close = () => dialog.value.close();
defineExpose({ open, close });
</script>

<template>
	<uni-popup ref="dialog" :mask-click="false" background-color="#fff">
		<div class="loadingContent flex gap-10 justify-center items-center">
			<div class="text-center text-bold text-2xl whitespace-nowrap">
				加载中
			</div>
			<image
				mode="widthFix"
				style="width: 70px"
				src="../static/univ.png"
			></image>
		</div>
	</uni-popup>
</template>

<style>
.loadingContent {
	width: 50vw;
	height: 4rem;
	padding: 1rem;
}
</style>
