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
const darkTheme = inject("darkTheme");
const searchContent = reactive({
    major: "",
    school: "",
});

const option = ref({
    title: {
        text: "历年计划数",
        left: "center",
        textStyle: {
            color: darkTheme ? "#c0c0c0" : "#333",
        },
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
            color: "#0284c7",
        },
    ],
});

onMounted(() => {
    axios.get("/list/sums").then((response) => {
        option.value.series[0].data = response.data;
    });

    inputRef.value.focus();
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
            class="text-center gradient-title from-cyan-500 via-sky-600 to-blue-800 mt-10 lg:md-15"
        >
            <div
                class="font-bold text-5xl md:text-6xl lg:text-7xl mb-1 md:mb-3 lg:mb-5"
            >
                MyUNIV
            </div>
            <div class="font-bold text-2xl md:text-3xl lg:text-4xl">
                高考志愿填报决策分析系统
            </div>
        </div>
        <div class="text-center mt-8 lg:mt-10">
            <div class="font-bold text-base md:text-lg lg:text-xl lg:mb-2">
                第二十三届全国学生信息素养提升实践活动获奖作品
            </div>
            <div class="text-base md:text-lg lg:text-xl lg:mb-1">孙奕凡</div>
            <div class="text-base md:text-lg lg:text-xl lg:mb-1">
                浙江省杭州高级中学
            </div>
        </div>
    </div>
    <div class="mt-10 flex justify-center md:mt-12">
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
