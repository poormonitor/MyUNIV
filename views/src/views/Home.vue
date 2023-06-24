<script setup>
import { Search } from "@vicons/ionicons5";
import * as echarts from "echarts";
import { useRouter } from "vue-router";

const collapsed = inject("collapsed");
const axios = inject("axios");
const router = useRouter();
const inputRef = ref(null);
const searchContent = ref(null);

let option = {
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
};

onMounted(() => {
    inputRef.value.focus();

    var myChart = echarts.init(document.getElementById("main-chart"));
    myChart.setOption(option);
    window.addEventListener("resize", function (event) {
        myChart.resize();
    });

    axios.get("/list/sums").then((response) => {
        option.series[0].data = response.data;
        myChart.setOption(option);
    });
});

const goQuery = () => {
    router.push({
        name: "query",
        query: {
            major: searchContent.value,
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
            <span class="whitespace-nowrap md:text-lg">专业</span>
            <n-input
                ref="inputRef"
                @keyup.enter="goQuery"
                v-model:value="searchContent"
                size="large"
                placeholder="搜索"
            >
                <template #prefix>
                    <n-icon :component="Search" />
                </template>
            </n-input>
            <n-button :size="collapsed ? 'medium' : 'large'" @click="goQuery">
                检索
            </n-button>
        </div>
    </div>
    <div class="mx-10 mt-10">
        <div class="mx-10 md:mx-auto md:w-[90vw] xl:w-[60vw]">
            <div id="main-chart" style="width: auto; height: 300px"></div>
        </div>
        <div class="mx-10 md:mx-auto md:w-[90vw] xl:w-[70vw]">
            <Intro class="my-8 md:my-12"></Intro>
        </div>
    </div>
</template>
