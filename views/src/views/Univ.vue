<script setup lang="jsx">
import { useRoute } from "vue-router";
import { provinces } from "../const";
import { getMustString } from "../func";
import { onMounted } from "vue";
import * as echarts from "echarts";
import { Close, Add } from "@vicons/ionicons5";
import { useMyStore } from "../stores/my";
import { useUserStore } from "../stores/user";

const axios = inject("axios");
const userStore = useUserStore();
const myStore = useMyStore();
const route = useRoute();

const tags = await axios.get("/list/tags").then((response) => response.data);
const data = await axios
    .get("/get/univ", { params: { sid: route.params.sid } })
    .then((response) => response.data);

onMounted(() => {
    let totalChart = echarts.init(document.getElementById("total"));
    let totalChartdata = data.ranks.reduce((accumulator, currentObject) => {
        const { year, schedule } = currentObject[0];
        let counter = accumulator.find((item) => item[0] == year);
        if (!counter) {
            accumulator.push([year, schedule]);
        } else {
            counter[1] += schedule;
        }
        return accumulator;
    }, []);
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
    let rankChartdata = data.ranks.reduce((accumulator, currentObject) => {
        const { year, rank } = currentObject[0];
        let counter = accumulator.find((item) => item[0] == year);
        if (!counter) {
            accumulator.push([year, rank]);
        } else {
            counter[1] = Math.max(rank, counter[1]);
        }
        return accumulator;
    }, []);
    rankChartdata.sort((a, b) => a[0] - b[0]);
    let rankChartoption = {
        title: {
            left: "center",
            text: "历年(最高)位次号",
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

const rankByYear = ref(true);
const rankCurrentItem = ref(null);
const rankData = ref([]);
const rankDataFiltered = ref([]);
const rankSelectOptions = computed(() =>
    rankData.value.map((e) => ({ value: e[0], label: e[0] }))
);
const rankColumns = [
    {
        title: "年份",
        key: "year",
        render: (row) => row[0].year,
        className: "whitespace-nowrap",
    },
    {
        title: "专业",
        className: "whitespace-nowrap",
        key: "major",
        render: (row) => (
            <RouterLink
                class="text-sky-800 hover:text-sky-900 transition"
                to={{ name: "major", params: { mid: row[1].mid } }}
            >
                {row[1].mname}
            </RouterLink>
        ),
    },
    {
        title: "位次号",
        className: "whitespace-nowrap",
        key: "rank",
        render: (row) => row[0].rank,
    },
    {
        title: "分数线",
        className: "whitespace-nowrap",
        key: "score",
        render: (row) => row[0].score,
    },
    {
        title: "计划数",
        className: "whitespace-nowrap",
        key: "schedule",
        render: (row) => row[0].schedule,
    },
    {
        title: "备选",
        key: "major",
        render: (row) => (
            <n-button
                circle
                secondary
                class="!w-7 !h-7"
                type={myStore.has(row[0].mid) ? "error" : "info"}
                onClick={
                    myStore.has(row[0].mid)
                        ? () => delMajor(row[0].mid)
                        : () => addMajor(row[0].mid)
                }
            >
                {{
                    icon: () => (
                        <n-icon
                            component={myStore.has(row[0].mid) ? Close : Add}
                        ></n-icon>
                    ),
                }}
            </n-button>
        ),
    },
];

const addMajor = (mid) => {
    if (!userStore.uid) return message.info("请先登录");
    axios.post("/user/major", { my: myStore.t_add(mid) }).then((response) => {
        if (response.data.result === "success") myStore.add(mid);
    });
};

const delMajor = (mid) => {
    if (!userStore.uid) return message.info("请先登录");
    axios
        .post("/user/major", { my: myStore.t_remove(mid) })
        .then((response) => {
            if (response.data.result === "success") myStore.remove(mid);
        });
};

watch(
    rankByYear,
    (val) => {
        rankData.value = Array.from(
            data.ranks.reduce((accumulator, currentObject) => {
                let tag;
                if (val) tag = currentObject[0].year;
                else tag = currentObject[1].mname;
                if (!accumulator.has(tag)) {
                    accumulator.set(tag, []);
                }
                accumulator.get(tag).push(currentObject);
                return accumulator;
            }, new Map())
        );
        rankData.value.sort((a, b) => b[0] - a[0]);
        rankCurrentItem.value = rankData.value[0][0];
    },
    { immediate: true }
);
watch(
    rankCurrentItem,
    (val) => {
        let rank_data = rankData.value.find((item) => item[0] == val)[1];
        if (rankByYear.value) rank_data.sort((a, b) => a[0].rank - b[0].rank);
        else rank_data.sort((a, b) => a[0].year - b[0].year);
        rankDataFiltered.value = rank_data;
    },
    { immediate: true }
);

const mustByYear = ref(true);
const mustCurrentItem = ref(null);
const mustData = ref([]);
const mustDataFiltered = ref([]);
const mustSelectOptions = computed(() =>
    mustData.value.map((e) => ({ value: e[0], label: e[0] }))
);
const mustColumns = [
    { title: "年份", key: "year", className: "whitespace-nowrap" },
    { title: "专业", key: "mname", className: "whitespace-nowrap" },
    {
        title: "必选科目",
        className: "whitespace-nowrap",
        key: "must",
        render: (row) => getMustString(row.must),
    },
    { title: "包含专业", key: "include" },
];
watch(
    mustByYear,
    (val) => {
        mustData.value = Array.from(
            data.musts.reduce((accumulator, currentObject) => {
                let tag;
                if (val) tag = currentObject.year;
                else tag = currentObject.mname;
                if (!accumulator.has(tag)) {
                    accumulator.set(tag, []);
                }
                accumulator.get(tag).push(currentObject);
                return accumulator;
            }, new Map())
        );
        mustData.value.sort((a, b) => b[0] - a[0]);
        mustCurrentItem.value = mustData.value[0][0];
    },
    { immediate: true }
);
watch(
    mustCurrentItem,
    (val) => {
        let must_data = mustData.value.find((item) => item[0] == val)[1];
        if (mustByYear.value) must_data.sort((a, b) => a.must - b.must);
        else must_data.sort((a, b) => a.year - b.year);
        mustDataFiltered.value = must_data;
    },
    { immediate: true }
);
</script>

<template>
    <div>
        <p class="text-4xl font-bold mb-2">
            {{ data.uname }}
        </p>
        <div class="mb-4 text-xl">
            {{ provinces[data.province] }}
        </div>
        <div class="mb-4 flex flex-wrap gap-2" v-if="data.utags">
            <n-tag type="info" v-for="item in data.utags">
                {{ tags.find((v) => v.tid == item).tname }}
            </n-tag>
        </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-8">
        <div id="total" class="center" style="width: auto; height: 250px"></div>
        <div id="rank" class="center" style="width: auto; height: 250px"></div>
    </div>
    <div class="mt-12 mb-10">
        <n-form class="flex gap-x-12" label-placement="left">
            <div class="text-2xl font-bold">历年投档信息</div>
            <n-form-item label="按年分类">
                <n-switch v-model:value="rankByYear"></n-switch>
            </n-form-item>
            <n-form-item label="分类项目">
                <div class="min-w-32">
                    <n-select
                        v-model:value="rankCurrentItem"
                        :consistent-menu-width="false"
                        :options="rankSelectOptions"
                    />
                </div>
            </n-form-item>
        </n-form>
        <n-data-table
            size="small"
            :data="rankDataFiltered"
            :columns="rankColumns"
        ></n-data-table>
    </div>
    <n-divider></n-divider>
    <div class="mt-10">
        <n-form class="flex gap-x-12" label-placement="left">
            <div class="text-2xl font-bold">必选科目要求</div>
            <n-form-item label="按年分类">
                <n-switch v-model:value="mustByYear"></n-switch>
            </n-form-item>
            <n-form-item label="分类项目">
                <div class="min-w-32">
                    <n-select
                        v-model:value="mustCurrentItem"
                        :consistent-menu-width="false"
                        :options="mustSelectOptions"
                    />
                </div>
            </n-form-item>
        </n-form>
        <n-data-table
            size="small"
            :data="mustDataFiltered"
            :columns="mustColumns"
        ></n-data-table>
    </div>
</template>
