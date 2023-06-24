<script setup>
const props = defineProps(["title"]);
</script>

<template>
    <div class="bg-gray-400/10 rounded-2xl p-5 md:p-8 md:mx-2 shadow">
        <p class="text-lg md:text-2xl font-bold">{{ props.title }}</p>
        <p class="pt-2 md:text-lg"><slot name="content"></slot></p>
    </div>
</template>