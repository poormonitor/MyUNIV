<script setup lang="jsx">
import {
    CaretDown,
    ExitOutline,
    LockClosedOutline,
    SettingsOutline,
} from "@vicons/ionicons5";
import { useRoute, useRouter } from "vue-router";
import { useMyStore } from "../stores/my";
import { useUserStore } from "../stores/user";
import PasswordSetter from "./PasswordSetter.vue";

const userStore = useUserStore();
const myStore = useMyStore();

const router = useRouter();
const route = useRoute();

const showPasswd = ref(false);

const renderIcon = (icon) => <n-icon component={icon}></n-icon>;

const options = [
    {
        label: "修改密码",
        key: "pw",
        icon: () => renderIcon(LockClosedOutline),
        target: () => {
            showPasswd.value = true;
        },
    },
    {
        label: "后台管理",
        key: "admin",
        icon: () => renderIcon(SettingsOutline),
        target: () => {
            router.push({ name: "admin" });
        },
    },
    {
        label: "退出登录",
        key: "logout",
        icon: () => renderIcon(ExitOutline),
        target: () => {
            userStore.logout();
            if (route.meta.requiresAuth) router.push({ name: "home" });
        },
    },
];

const handleSelect = (key) => {
    options.find((item) => item.key == key).target();
};

const selectOptions = computed(() => {
    let options = [];
    for (var i = 0; i < myStore.newList; i++) {
        options.push({ label: `备选列表 ${i + 1}`, value: i });
    }
    options.push({ label: "新列表", value: "new" });
    return options;
});
</script>

<template>
    <div class="w-32 flex items-center">
        <n-select
            :options="selectOptions"
            v-model:value="myStore.order"
        ></n-select>
    </div>
    <div class="flex items-center ml-4" v-if="userStore.uid">
        <PasswordSetter v-model:show="showPasswd" />
        <n-dropdown trigger="hover" :options="options" @select="handleSelect">
            <div
                class="flex items-center gap-x-1 hover:text-cyan-700 transition"
            >
                <span class="whitespace-nowrap">{{ userStore.name }}</span>
                <n-icon size="0.7rem" :component="CaretDown"></n-icon>
            </div>
        </n-dropdown>
    </div>
</template>
