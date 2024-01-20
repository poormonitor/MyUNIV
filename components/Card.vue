<script setup>
const props = defineProps(['title']);
</script>

<template>
	<div class="card mb-20 p-20">
		<p class="text-xl text-bold">{{ props.title }}</p>
		<p class="pt-10"><slot name="content"></slot></p>
	</div>
</template>

<style>
.card {
	--tw-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
	--tw-shadow-colored: 0 1px 3px 0 var(--tw-shadow-color),
		0 1px 2px -1px var(--tw-shadow-color);
	box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),
		var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);
	background-color: #ffffff;
	border-radius: 1rem;
}
</style>
