<script setup lang="jsx">
import { onActivated, onMounted } from "vue";
import { getMustString, findMaxValue, base64toBlob } from "../func";
import { useMyStore } from "../stores/my";
import { Add, Close } from "@vicons/ionicons5";

import * as echarts from "echarts/core";
import { TitleComponent, SingleAxisComponent } from "echarts/components";
import { ScatterChart } from "echarts/charts";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
    TitleComponent,
    SingleAxisComponent,
    ScatterChart,
    CanvasRenderer,
    UniversalTransition,
]);

var table = null;
const data = reactive({ total: 0, list: [] });
const axios = inject("axios");
const loading = ref(true);
const rank_years = ref([]);
const must_years = ref([]);
const myStore = useMyStore();
const info = reactive({
    year: 0,
    standard: 0,
});

const goQuery = () => {
    axios
        .post("/get/majors", { ...info, majors: myStore.get() })
        .then((response) => {
            data.total = response.data.total;

            let result = [];
            response.data.result.forEach((elem, index) => {
                elem[4] = index + 1;
                result[index] = elem;
            });
            data.list = result;

            loading.value = false;
        });
};

const renderTable = (val) => {
    let options = {
        singleAxis: {
            top: "middle",
            left: "2%",
            left: "2%",
            height: "0",
            type: "value",
            boundaryGap: false,
        },
        textStyle: {
            fontFamily: ["Inter", "Noto Sans SC"],
            fontWeight: "bold",
        },
        series: {
            coordinateSystem: "singleAxis",
            type: "scatter",
            data: val.map((item) => [item[2].rank]),
        },
    };

    table.setOption(options);
};

watch(() => data.list, renderTable);

Promise.all([
    axios.get("/list/ranks").then((response) => {
        rank_years.value = response.data.map((item) => ({
            label: item,
            value: item,
        }));
        info.year = Math.max(...response.data);
    }),
    axios.get("/list/musts").then((response) => {
        must_years.value = response.data.map((item) => ({
            label: item,
            value: item,
        }));
        let current = new Date().getFullYear();
        info.standard = findMaxValue(response.data, current);
    }),
]).then(() => {
    watch(info, goQuery, { immediate: true });
    watch(() => myStore.order, goQuery);
});

onActivated(goQuery);
onMounted(() => {
    table = echarts.init(document.getElementById("table"));
    window.addEventListener("resize", () => {
        table.resize();
    });
});

const removeItem = (id) => {
    myStore.remove(id);
    data.total -= 1;
    data.list = data.list.filter((item) => item[0].mid != id);
};

const resetItem = () => {
    myStore.reset();
    data.total = 0;
    data.list = [];
};

const downloadExcel = () => {
    axios
        .post("/get/table", { ...info, majors: myStore.get() })
        .then((response) => {
            const blob = base64toBlob(response.data.file);
            const downloadLink = document.createElement("a");

            downloadLink.href = URL.createObjectURL(blob);
            downloadLink.setAttribute(
                "download",
                `MyUNIV_Export_${new Date().getTime()}.xlsx`
            );

            downloadLink.click();

            URL.revokeObjectURL(downloadLink.href);
        })
        .catch((error) => {
            console.error("Error downloading the file:", error);
        });
};

const tableColumns = [
    { title: "排序", key: "index", render: (row) => row[4] },
    {
        title: "学校名称",
        key: "univ",
        sorter: (row1, row2) => row1[1].sid - row2[1].sid,
        render: (row) => (
            <router-link
                class="text-sky-800 hover:text-sky-900 transition"
                to={{ name: "univ", params: { sid: row[1].sid } }}
            >
                {row[1].uname}
            </router-link>
        ),
    },
    {
        title: "专业名称",
        key: "major",
        render: (row) => (
            <router-link
                class="text-sky-800 hover:text-sky-900 transition"
                to={{ name: "major", params: { mid: row[0].mid } }}
            >
                {row[0].mname}
            </router-link>
        ),
    },
    {
        title: "计划数",
        key: "schedule",
        render: (row) => <span>{row[2].schedule}</span>,
    },
    {
        title: "年份",
        key: "major",
        render: (row) => <span>{row[2].year}</span>,
    },
    {
        title: "位次号",
        key: "major",
        sorter: (row1, row2) => row1[2].rank - row2[2].rank,
        render: (row) => <span>{row[2].rank}</span>,
    },
    {
        title: "分数",
        key: "major",
        render: (row) => <span>{row[2].score}</span>,
    },
    {
        title: "选考科目要求",
        key: "major",
        render: (row) => <span>{getMustString(row[3].must)}</span>,
    },
    {
        title: "选科标准",
        key: "major",
        render: (row) => <span>{row[3].year}</span>,
    },
    {
        title: "删除备选",
        key: "delete",
        render: (row) => (
            <n-button
                circle
                secondary
                class="!w-7 !h-7"
                type="error"
                onClick={() => removeItem(row[0].mid)}
            >
                {{
                    icon: () => <n-icon component={Close}></n-icon>,
                }}
            </n-button>
        ),
    },
];
</script>

<template>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] my-8">
        <div class="w-full mx-auto">
            <div class="flex flex-col sm:flex-row justify-between">
                <n-statistic label="共计收藏了" tabular-nums>
                    {{ myStore.count }}
                    <template #suffix> 个专业 </template>
                </n-statistic>
                <div
                    class="flex gap-x-4 justify-between sm:justify-end items-center mt-4"
                >
                    <div class="flex flex-col sm:flex-row gap-2">
                        <n-popconfirm
                            v-if="data.total"
                            @positive-click="resetItem"
                        >
                            <template #trigger>
                                <n-button
                                    strong
                                    secondary
                                    size="small"
                                    type="error"
                                >
                                    删除所有
                                </n-button>
                            </template>
                            确认删除？
                        </n-popconfirm>
                        <n-button
                            strong
                            secondary
                            size="small"
                            type="error"
                            @click="() => myStore.removeList()"
                            v-else-if="myStore.order !== 0"
                        >
                            删除列表
                        </n-button>
                        <n-button
                            strong
                            secondary
                            size="small"
                            type="primary"
                            @click="downloadExcel"
                            v-if="data.total"
                            >下载表格</n-button
                        >
                    </div>
                    <n-form-item class="w-32" label="投档数据">
                        <n-select
                            v-model:value="info.year"
                            max-tag-count="responsive"
                            :options="rank_years"
                        ></n-select>
                    </n-form-item>
                    <n-form-item class="w-32" label="选考标准">
                        <n-select
                            v-model:value="info.standard"
                            max-tag-count="responsive"
                            :options="must_years"
                        ></n-select>
                    </n-form-item>
                </div>
            </div>
            <div id="table" class="h-12 mb-5"></div>
            <n-data-table
                :columns="tableColumns"
                :data="data.list"
                :loading="loading"
                size="small"
                class="whitespace-nowrap"
                @update:page="goQuery"
            />
        </div>
    </div>
</template>
