<script setup>
import { SchoolOutline, BookOutline } from "@vicons/ionicons5";
import { useRouter } from "vue-router";

import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
} from "echarts/components";
import { LabelLayout, UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import { onActivated } from "vue";

use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LineChart,
    LabelLayout,
    UniversalTransition,
    CanvasRenderer,
]);

const collapsed = inject("collapsed");
const axios = inject("axios");
const router = useRouter();
const inputRef = ref(null);
const searchContent = reactive({
    major: "",
    school: "",
});

const option = ref({
    title: {
        text: "历年计划数",
        left: "center",
    },
    textStyle: {
        fontFamily: ["Inter", "Noto Sans SC"],
        fontWeight: "bold",
    },
    grid: {
        left: "1%",
        right: "1%",
        bottom: "1%",
        containLabel: true,
    },
    tooltip: {
        trigger: "axis",
    },
    xAxis: {
        type: "category",
    },
    yAxis: {
        type: "value",
    },
    series: [
        {
            data: [],
            name: "计划数",
            type: "line",
            smooth: true,
            color: "#383838",
        },
    ],
});

onActivated(() => {
    inputRef.value.focus();
});

onMounted(() => {
    axios.get("/list/sums").then((response) => {
        option.value.series[0].data = response.data;
    });
});

const goQuery = () => {
    router.push({
        name: "query",
        query: {
            major: searchContent.major ? searchContent.major : undefined,
            school: searchContent.school ? searchContent.school : undefined,
        },
    });
};
</script>

<template>
    <div class="mx-16 md:mx-auto md:w-[90vw] xl:w-[70vw]">
        <div
            class="text-center gradient-title from-cyan-500 via-sky-600 to-blue-800 mt-10"
        >
            <div class="mb-1 font-bold text-5xl md:text-6xl md:mb-3">
                MyUNIV
            </div>
            <div class="text-2xl font-bold md:text-3xl">
                高考志愿填报决策分析系统
            </div>
        </div>
    </div>
    <div class="mt-8 flex justify-center md:mt-12">
        <div class="mx-8 flex items-center gap-x-4 md:mx-auto md:w-[40vw]">
            <span class="whitespace-nowrap md:text-lg">搜索</span>
            <n-input
                ref="inputRef"
                @keyup.enter="goQuery"
                v-model:value="searchContent.school"
                :size="collapsed ? 'medium' : 'large'"
                placeholder="学校"
            >
                <template #prefix>
                    <n-icon :component="SchoolOutline" />
                </template>
            </n-input>
            <n-input
                ref="input2Ref"
                @keyup.enter="goQuery"
                v-model:value="searchContent.major"
                :size="collapsed ? 'medium' : 'large'"
                placeholder="专业"
            >
                <template #prefix>
                    <n-icon :component="BookOutline" />
                </template>
            </n-input>
            <n-button :size="collapsed ? 'medium' : 'large'" @click="goQuery">
                检索
            </n-button>
        </div>
    </div>
    <div class="md:mx-10 mt-10">
        <div class="mx-10 md:mx-auto md:w-[90vw] xl:w-[60vw]">
            <div class="chart" style="width: auto; height: 300px">
                <v-chart :option="option" autoresize />
            </div>
        </div>
        <div class="mx-10 md:mx-auto md:w-[90vw] xl:w-[70vw]">
            <Intro class="my-8 md:my-12"></Intro>
        </div>
    </div>
</template>
