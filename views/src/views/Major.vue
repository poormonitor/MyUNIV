<script setup lang="jsx">
import { useRoute } from "vue-router";
import { useMyStore } from "../stores/my";
import { useUserStore } from "../stores/user";
import { getMustString } from "../func";
import { onMounted } from "vue";
import { message } from "../discrete";

import * as echarts from "echarts/core";
import { LineChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
} from "echarts/components";
import { LabelLayout, UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LineChart,
    LabelLayout,
    UniversalTransition,
    CanvasRenderer,
]);

const axios = inject("axios");
const route = useRoute();
const myStore = useMyStore();

const data = await axios
    .get("/get/major", { params: { mid: route.params.mid } })
    .then((response) => response.data);

data.ranks.sort((a, b) => a.year - b.year);
data.musts.sort((a, b) => a.year - b.year);

const tags = Array.from(
    data.musts.reduce((ac, ob) => {
        if (
            data.value.mname.includes(ob.mname) ||
            ob.mname.includes(data.mname)
        )
            ob.include.split("、").forEach((elem) => {
                if (elem) ac.add(elem);
            });
        return ac;
    }, new Set())
);

onMounted(() => {
    let totalChart = echarts.init(document.getElementById("total"));
    let totalChartdata = data.ranks.map((item) => [item.year, item.schedule]);
    totalChartdata.sort((a, b) => a[0] - b[0]);
    let totalChartoption = {
        title: {
            left: "center",
            text: "历年计划数",
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
                data: totalChartdata,
                name: "计划数",
                type: "line",
                smooth: true,
                color: "#78c2ad",
            },
        ],
    };
    totalChart.setOption(totalChartoption);

    let rankChart = echarts.init(document.getElementById("rank"));
    let rankChartdata = data.ranks.map((item) => [item.year, item.rank]);
    rankChartdata.sort((a, b) => a[0] - b[0]);
    let rankChartoption = {
        title: {
            left: "center",
            text: "历年位次号",
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
                data: rankChartdata,
                name: "位次号",
                type: "line",
                smooth: true,
                color: "#78c2ad",
            },
        ],
    };
    rankChart.setOption(rankChartoption);

    window.addEventListener("resize", function (event) {
        totalChart.resize();
        rankChart.resize();
    });
});

const rankColumns = [
    {
        title: "年份",
        key: "year",
        className: "whitespace-nowrap",
    },
    {
        title: "专业",
        className: "whitespace-nowrap",
        key: "mname",
        render: () => data.mname,
    },
    {
        title: "位次号",
        className: "whitespace-nowrap",
        key: "rank",
    },
    {
        title: "分数线",
        className: "whitespace-nowrap",
        key: "score",
    },
    {
        title: "计划数",
        className: "whitespace-nowrap",
        key: "schedule",
    },
];

const mustColumns = [
    { title: "年份", key: "year", className: "whitespace-nowrap" },
    { title: "专业", key: "mname", className: "whitespace-nowrap" },
    {
        title: "必选科目",
        className: "whitespace-nowrap",
        key: "must",
        render: (row) => getMustString(row.must),
    },
    { title: "包含专业", className: "whitespace-nowrap", key: "include" },
];
</script>

<template>
    <div class="mb-8">
        <div
            class="flex flex-col md:flex-row md:justify-between gap-y-2 gap-x-4 items-start md:items-center mb-4"
        >
            <div>
                <p class="text-4xl font-bold mb-2">
                    {{ data.mname }}
                </p>
                <div class="text-xl">
                    <router-link
                        :to="{ name: 'univ', params: { sid: data.univ.sid } }"
                        class="text-sky-800 hover:text-sky-900 transition"
                    >
                        {{ data.univ.uname }}
                    </router-link>
                </div>
            </div>
            <n-button
                :type="myStore.has(data.mid) ? 'error' : 'info'"
                secondary
                @click="
                    () =>
                        myStore.has(data.mid)
                            ? myStore.remove(data.mid)
                            : myStore.add(data.mid)
                "
            >
                {{ myStore.has(data.mid) ? "删除备选" : "加入备选" }}
            </n-button>
        </div>
        <div class="mb-4 flex flex-wrap gap-2" v-if="tags">
            <n-tag type="info" v-for="item in tags">
                {{ item }}
            </n-tag>
        </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-8">
        <div id="total" class="center" style="width: auto; height: 250px"></div>
        <div id="rank" class="center" style="width: auto; height: 250px"></div>
    </div>
    <div class="mt-12 mb-10">
        <div class="text-2xl font-bold mb-4">历年投档信息</div>
        <n-data-table
            size="small"
            :data="data.ranks"
            :columns="rankColumns"
        ></n-data-table>
    </div>
    <n-divider></n-divider>
    <div class="mt-10 mb-10">
        <div class="text-2xl font-bold mb-4">必选科目要求</div>
        <n-data-table
            size="small"
            :data="data.musts"
            :columns="mustColumns"
        ></n-data-table>
    </div>
</template>
