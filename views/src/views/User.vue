<script setup lang="jsx">
import { useUserStore } from "../stores/user";

const axios = inject("axios");
const userStore = useUserStore();

const data = ref([]);
const cnt = ref(0);
const loading = ref(true);
const UserKeyword = ref(null);
const CurrentUID = ref(null);
const ShowModify = ref(false);

const pagination = reactive({
    page: 1,
    pageCount: 0,
    pageSize: 10,
});

const tableColumns = [
    { key: "uid", title: "用户名" },
    { key: "name", title: "姓名" },
    {
        key: "last_login",
        title: "最近登录",
        render: (row) => row.last_login.replace("T", " "),
    },
    {
        key: "admin",
        title: "管理员",
        render: (row) => (
            <n-switch
                value={row.admin}
                disabled={row.uid === userStore.uid}
                on-update:value={() => SwitchAdmin(row.uid)}
            >
                {{
                    checked: () => "是",
                    unchecked: () => "否",
                }}
            </n-switch>
        ),
    },
    {
        key: "passwd",
        title: "密码",
        render: (row) => (
            <n-button
                size="small"
                secondary
                on-click={() => {
                    ShowModify.value = true;
                    CurrentUID.value = row.uid;
                }}
            >
                修改密码
            </n-button>
        ),
    },
    {
        key: "delete",
        title: "删除",
        render: (row) => (
            <n-popconfirm on-positive-click={() => DeleteUser(row.uid)}>
                {{
                    trigger: () => (
                        <n-button
                            size="small"
                            disabled={row.uid === userStore.uid}
                            type="error"
                            secondary
                        >
                            删除用户
                        </n-button>
                    ),
                }}
            </n-popconfirm>
        ),
    },
];

const SwitchAdmin = (uid) => {
    let perm = !data.value.find((item) => item.uid === uid)?.admin;
    axios
        .post("/users/admin", {
            uid: uid,
            admin: perm,
        })
        .then((response) => {
            if (response.data.result === "success") {
                data.value.find((item) => item.uid === uid).admin = perm;
            }
        });
};

const DeleteUser = (uid) => {
    axios
        .post("/users/delete", {
            uid: uid,
        })
        .then((response) => {
            if (response.data.result === "success") {
                data.value = data.value.filter((item) => item.uid !== uid);
            }
        });
};

const fetchData = () => {
    loading.value = true;
    axios
        .get("/users/list", {
            params: {
                s: UserKeyword.value,
                page: pagination.page,
            },
        })
        .then((response) => {
            if (response.data.cnt) {
                data.value = response.data.users;
                cnt.value = response.data.cnt;
                pagination.pageCount = Math.ceil(
                    cnt.value / pagination.pageSize
                );
                loading.value = false;
            }
        });
};

fetchData();
</script>

<template>
    <PasswordModify :uid="CurrentUID" v-model:show="ShowModify" />
    <p class="text-xl md:text-3xl font-bold pb-4 pt-2">用户管理</p>
    <div>
        <div class="flex justify-between gap-x-4 mx-8 mb-6 mt-3">
            <div class="flex gap-x-4 items-center">
                <n-input @keyup.enter="fetchData" v-model:value="UserKeyword" />
                <n-button @click="fetchData">过滤</n-button>
            </div>
            <n-pagination
                v-model:page="pagination.page"
                :page-count="pagination.pageCount"
                @update:page="fetchData"
            />
        </div>
        <n-data-table
            :data="data"
            :columns="tableColumns"
            :loading="loading"
            class="whitespace-nowrap"
        />
    </div>
</template>
