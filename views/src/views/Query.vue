<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { provinces, majors } from "../const";
import {
    getMustString,
    fixInteger,
    filterEmptyObject,
    findMaxValue,
} from "../func";
import { useMyStore } from "../stores/my";
import { message } from "../discrete";
import { useUserStore } from "../stores/user";
import { Close, Add } from "@vicons/ionicons5";
import { useDialog } from "naive-ui";
import { onMounted } from "vue";
import Cookies from "js-cookie";

const route = useRoute();
const router = useRouter();
const axios = inject("axios");
const dialog = useDialog();
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
    rank: null,
    year: 0,
    school: "",
    major: "",
    rank_range: null,
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

const score = reactive({ show: false, year: info.year, score: 600 });

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

        if (!info.year) score.year = info.year = Math.max(...response.data);
    }),
    axios.get("/list/musts").then((response) => {
        must_years.value = response.data.map((item) => ({
            label: item,
            value: item,
        }));
        let current = new Date().getFullYear();
        let currentMonth = new Date().getMonth();
        if (currentMonth >= 7) current += 1;
        info.standard = findMaxValue(response.data, current);
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
        if (pagination.page > pagination.pageCount) pagination.page = 1;
        loading.value = false;
    });
};

const switchPage = () => {
    let count = document.getElementById("divider");
    if (count) count.scrollIntoView({ behavior: "smooth" });
    goQuery();
};

const handleQueryKeyUp = (event) => {
    if (event.key === "Enter") goQuery();
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
                        ? () => {
                              myStore.remove(row[0].mid);
                          }
                        : () => {
                              myStore.add(row[0].mid);
                          }
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

const fetchRank = () => {
    axios
        .get("/get/score", { params: { score: score.score, year: score.year } })
        .then((response) => {
            if (response.data) {
                info.rank = response.data.rank;
                score.show = false;
            }
        });
};

onMounted(() => {
    if (Cookies.get("agreement") !== "true")
        dialog.info({
            title: "免责声明",
            content: () => (
                <div class="my-6 mx-4">
                    本页面提供数据来自政府教育考试机构。
                    系统已经采取最佳可行算法自动处理相关数据，但仍可能存在必选科目匹配错误等信息有误情况。
                    本系统仅供辅助查询，请您以相关学校以及教育考试机构官方数据为准。
                    网站运营者不承担有关数据正确性的个别及连带责任。
                </div>
            ),
            positiveText: "确定",
            maskClosable: false,
            onPositiveClick: () => {
                Cookies.set("agreement", "true", { expires: 3650 });
            },
        });
});
</script>

<template>
    <n-modal
        v-model:show="score.show"
        title="分数转换"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="fetchRank"
    >
        <n-form class="px-8 pt-8">
            <n-form-item label="年份">
                <n-select
                    v-model:value="score.year"
                    :options="rank_years"
                ></n-select>
            </n-form-item>
            <n-form-item label="分数">
                <n-input-number
                    class="w-full"
                    v-model:value="score.score"
                ></n-input-number>
            </n-form-item>
        </n-form>
    </n-modal>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[75vw] pt-8 pb-4">
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
                <n-input
                    v-model:value="info.school"
                    @keyup="handleQueryKeyUp"
                ></n-input>
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
                <n-input
                    v-model:value="info.major"
                    @keyup="handleQueryKeyUp"
                ></n-input>
            </n-form-item>
            <n-form-item label="位次号">
                <div class="flex gap-x-2">
                    <n-input-number v-model:value="info.rank"></n-input-number>
                    <n-button @click="score.show = true"> 转换 </n-button>
                </div>
            </n-form-item>
            <n-form-item label="区间">
                <n-input-number
                    v-model:value="info.rank_range"
                ></n-input-number>
            </n-form-item>
            <n-form-item label="投档数据">
                <n-select
                    v-model:value="info.year"
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
                    :options="must_years"
                ></n-select>
            </n-form-item>
            <n-form-item label="一致优先">
                <n-switch v-model:value="info.accordation" />
            </n-form-item>
        </n-form>
        <div class="flex justify-center">
            <div class="w-32">
                <n-button @click="goQuery" type="info" :block="true">
                    查找
                </n-button>
            </div>
        </div>

        <n-divider id="divider"></n-divider>
        <div class="w-full mx-auto">
            <div class="flex justify-between items-end mb-4 flex-wrap gap-y-3">
                <n-statistic
                    label="共计找到了"
                    tabular-nums
                    class="hidden md:block"
                >
                    {{ data.total }}
                    <template #suffix> 个专业 </template>
                </n-statistic>
                <span class="md:hidden text-lg">
                    共计找到了 <b>{{ data.total }}</b> 个专业
                </span>
                <n-pagination
                    class="mb-2 ml-auto"
                    v-model:page="pagination.page"
                    :page-count="pagination.pageCount"
                    :page-slot="7"
                    @update:page="goQuery"
                    v-if="loading || data.total"
                />
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
                    :page-slot="7"
                    @update:page="switchPage"
                />
            </div>
            <n-empty class="mt-12 pb-8" description="什么也没找到" v-else></n-empty>
        </div>
    </div>
</template>
