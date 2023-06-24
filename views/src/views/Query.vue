<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { provinces, majors } from "../const";
import {
    getMustString,
    fixInteger,
    filterEmptyObject,
    compareObjects,
} from "../func";
import { useMyStore } from "../stores/my";
import { useUserStore } from "../stores/user";
import { Close, Add } from "@vicons/ionicons5";

const route = useRoute();
const router = useRouter();
const axios = inject("axios");
const myStore = useMyStore();
const userStore = useUserStore();

const tags = ref([]);
const rank_years = ref([]);
const must_years = ref([]);
const data = reactive({ total: 0, list: [] });
const loading = ref(true);
const pagination = reactive({
    page: 1,
    pageCount: 0,
    pageSize: 50,
});

const info = reactive({
    rank: "",
    year: 0,
    school: "",
    major: "",
    rank_range: "",
    utags: "",
    province: [],
    utags: [],
    nutags: [],
    mymust: [],
    standard: 0,
    accordation: false,
});
Object.assign(info, route.query);
fixInteger(info, "province");
fixInteger(info, "utags");
fixInteger(info, "nutags");
fixInteger(info, "mymust");

axios.get("/list/tags").then((response) => {
    tags.value = response.data.map((item) => ({
        label: item.tname,
        value: item.tid,
    }));
});

Promise.all([
    axios.get("/list/ranks").then((response) => {
        rank_years.value = response.data.map((item) => ({
            label: item,
            value: item,
        }));
        if (!info.year) info.year = Math.max(...response.data);
    }),
    axios.get("/list/musts").then((response) => {
        must_years.value = response.data.map((item) => ({
            label: item,
            value: item,
        }));
        if (!info.standard) info.standard = Math.max(...response.data);
    }),
]).then(() => {
    goQuery();
});

const goQuery = () => {
    loading.value = true;
    info.page = pagination.page;
    router.push({ query: filterEmptyObject(info) });
    axios.post("/query", info).then((response) => {
        data.total = response.data.total;
        data.list = response.data.result;
        pagination.pageCount = Math.ceil(data.total / pagination.pageSize);
        loading.value = false;
    });
};

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

const tableColumns = [
    {
        title: "学校名称",
        key: "univ",
        render: (row) => (
            <router-link
                target="_blank"
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
                target="_blank"
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

const province_option = Object.keys(provinces)
    .slice(1)
    .map((item) => ({
        label: provinces[item],
        value: item,
    }));

const must_options = majors.slice(1).map((item, index) => ({
    label: item,
    value: index + 1,
}));
</script>

<template>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] my-8">
        <n-form class="grid grid-cols-2 gap-x-4 md:grid-cols-4 md:gap-x-8">
            <n-form-item label="省份">
                <n-select
                    v-model:value="info.province"
                    max-tag-count="responsive"
                    multiple
                    :options="province_option"
                ></n-select>
            </n-form-item>
            <n-form-item label="学校">
                <n-input v-model:value="info.school"></n-input>
            </n-form-item>
            <n-form-item label="标签(包含)">
                <n-select
                    v-model:value="info.utags"
                    max-tag-count="responsive"
                    multiple
                    :options="tags"
                ></n-select>
            </n-form-item>
            <n-form-item label="标签(不包含)">
                <n-select
                    v-model:value="info.nutags"
                    max-tag-count="responsive"
                    multiple
                    :options="tags"
                ></n-select>
            </n-form-item>
            <n-form-item label="专业">
                <n-input v-model:value="info.major"></n-input>
            </n-form-item>
            <n-form-item label="位次号">
                <n-input v-model:value="info.rank"></n-input>
            </n-form-item>
            <n-form-item label="区间">
                <n-input v-model:value="info.rank_range"></n-input>
            </n-form-item>
            <n-form-item label="投档数据">
                <n-select
                    v-model:value="info.year"
                    max-tag-count="responsive"
                    :options="rank_years"
                ></n-select>
            </n-form-item>
            <n-form-item class="col-span-2" label="选考科目">
                <n-checkbox-group :max="3" v-model:value="info.mymust">
                    <n-space item-style="display: flex;">
                        <n-checkbox
                            v-for="option in must_options"
                            :value="option.value"
                            :label="option.label"
                        />
                    </n-space>
                </n-checkbox-group>
            </n-form-item>
            <n-form-item label="选考标准">
                <n-select
                    v-model:value="info.standard"
                    max-tag-count="responsive"
                    :options="must_years"
                ></n-select>
            </n-form-item>
            <n-form-item label="一致优先">
                <n-switch v-model:value="info.accordation" />
            </n-form-item>
        </n-form>
        <div class="flex justify-center">
            <div class="w-32">
                <n-button @click="goQuery" type="info" :block="true"
                    >查找</n-button
                >
            </div>
        </div>

        <n-divider></n-divider>
        <div class="w-full mx-auto">
            <div class="mb-4">
                <n-statistic label="共计找到了" tabular-nums>
                    {{ data.total }}
                    <template #suffix> 个专业 </template>
                </n-statistic>
            </div>
            <div v-if="loading || data.total">
                <n-data-table
                    :columns="tableColumns"
                    :data="data.list"
                    :loading="loading"
                    size="small"
                    class="whitespace-nowrap"
                    @update:page="goQuery"
                />
                <n-pagination
                    class="justify-end mt-3 mb-8"
                    v-model:page="pagination.page"
                    :page-count="pagination.pageCount"
                    @update:page="goQuery"
                />
            </div>
            <n-empty class="mt-12" description="什么也没找到" v-else></n-empty>
        </div>
    </div>
</template>
