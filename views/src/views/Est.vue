<script setup lang="jsx">
const axios = inject("axios");
const data = ref([]);
const loading = ref(false);
const showModal = ref(false);
const userData = ref("");
const year = ref(null);
const rank = ref(0);
const rank_years = ref([]);

const goQuery = () => {
    let content = userData.value;
    if (!content || content == "") return;
    let lines = content.split("\n");
    let info = [];
    for (let line of lines) {
        let items = line.split("\t");
        if (items.length < 3) continue;
        info.push({
            uname: items[1],
            mname: items[2],
        });
    }

    showModal.value = false;
    loading.value = true;

    axios
        .post("/query/ranks", { list: info, year: year.value })
        .catch((_) => {
            showModal.value = true;
            loading.value = false;
        })
        .then((response) => {
            data.value = response.data.result;

            for (let i = 0; i < data.value.length; i++) {
                if (Number(data.value[i][2].rank) >= Number(rank.value)) {
                    data.value[i].push(true);
                    break;
                }
            }

            loading.value = false;
        });
};

axios
    .get("/list/ranks")
    .then((response) => {
        rank_years.value = response.data.map((item) => ({
            label: item,
            value: item,
        }));
        year.value = Math.max(...response.data);
    })
    .then(() => {
        showModal.value = true;
    });

onActivated(() => {
    if (!userData.value || userData.value == "") {
        showModal.value = true;
    }
});

const tableColumns = [
    {
        title: "学校名称",
        key: "univ",
        render: (row) => (
            <router-link
                class="text-sky-800 dark:text-sky-500 hover:text-sky-900 dark:hover:text-sky-600 transition"
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
                class="text-sky-800 dark:text-sky-500 hover:text-sky-900 dark:hover:text-sky-600 transition"
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
        render: (row) => (
            <span class={{ "text-red-500": row.length >= 4 }}>
                {row[2].rank}
            </span>
        ),
    },
    {
        title: "分数",
        key: "major",
        render: (row) => <span>{row[2].score}</span>,
    },
];
</script>

<template>
    <n-modal v-model:show="showModal">
        <n-card
            style="width: 600px"
            title="输入信息"
            :bordered="false"
            :mask-closable="false"
            :close-on-esc="false"
            size="huge"
            role="dialog"
            aria-modal="true"
        >
            <p class="mb-5">
                请从政府教育考试机构网站复制您的投档信息表,
                粘贴到下面的文本框中。每行数据依次为志愿序号，院校，专业。
            </p>
            <n-form>
                <n-form-item label="投档信息">
                    <n-input
                        type="textarea"
                        v-model:value="userData"
                        placeholder="请粘贴您的投档信息表"
                    />
                </n-form-item>
                <n-form-item label="位次号">
                    <n-input-number class="w-full" v-model:value="rank" />
                </n-form-item>
                <n-form-item label="年份">
                    <n-select v-model:value="year" :options="rank_years" />
                </n-form-item>
            </n-form>
            <template #footer>
                <div class="flex justify-end mb-4">
                    <n-button class="justify-self-end" @click="goQuery">
                        查询
                    </n-button>
                </div>
            </template>
        </n-card>
    </n-modal>

    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] my-8">
        <div class="mb-4 flex justify-center">
            <n-button @click="showModal = true">重新查询</n-button>
        </div>
        <div class="w-full mx-auto mb-20">
            <n-data-table
                :columns="tableColumns"
                :data="data"
                :loading="loading"
                size="small"
                class="whitespace-nowrap"
                @update:page="goQuery"
            />
        </div>
    </div>
</template>
