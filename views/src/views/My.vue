<script setup lang="jsx">
import { getMustString } from "../func";
import { useMyStore } from "../stores/my";
import { Add, Close } from "@vicons/ionicons5";

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
    axios.post("/get/my", info).then((response) => {
        data.total = response.data.total;
        data.list = response.data.result;
        myStore.my = data.list.map((item) => item[0].mid);
        loading.value = false;
    });
};

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
        info.standard = Math.max(...response.data);
    }),
]).then(() => {
    watch(info, goQuery, { immediate: true });
});

const removeItem = (id) => {
    axios.post("/user/major", { my: myStore.t_remove(id) }).then((response) => {
        if (response.data.result == "success") {
            myStore.remove(id);
            data.total -= 1;
            data.list = data.list.filter((item) => item[0].mid != id);
        }
    });
};

const tableColumns = [
    {
        title: "学校名称",
        key: "univ",
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

const cleanMajor = () => {
    axios.post("/user/major", { my: [] }).then((response) => {
        if (response.data.result == "success") {
            data.total = 0;
            data.list = [];
            myStore.reset();
        }
    });
};
</script>

<template>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] my-8">
        <div class="w-full mx-auto">
            <div class="mb-4 flex flex-col md:flex-row justify-between">
                <n-statistic label="共计收藏了" tabular-nums>
                    {{ data.total }}
                    <template #suffix> 个专业 </template>
                </n-statistic>
                <div class="flex gap-x-8 items-center">
                    <n-button
                        strong
                        secondary
                        type="error"
                        @click="cleanMajor"
                        v-if="data.total"
                        >删除所有</n-button
                    >
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
