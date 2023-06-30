<script setup lang="jsx">
import { useRoute, useRouter } from "vue-router";
import { NIcon } from "naive-ui";
import { FileTrayFull, Documents, People } from "@vicons/ionicons5";
import { useUserStore } from "../stores/user";

const collapsed = inject("collapsed");
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();

const renderIcon = (icon) => () => <NIcon component={icon}></NIcon>;

const renderLabel = (title, to) => () =>
    <router-link to={{ name: to }}>{title}</router-link>;

const menuOptions = [
    {
        label: renderLabel("用户管理", "user"),
        icon: renderIcon(People),
        key: "user",
    },
    {
        label: renderLabel("数据上传", "upload"),
        icon: renderIcon(Documents),
        key: "upload",
    },
    {
        label: renderLabel("添加标签", "tag"),
        icon: renderIcon(FileTrayFull),
        key: "tag",
    },
];

if (!userStore.admin) menuOptions.shift()
</script>

<template>
    <n-layout class="min-h-full pb-12">
        <n-layout-header bordered>
            <Header></Header>
        </n-layout-header>
        <n-layout class="admin-container" has-sider>
            <n-layout-sider
                bordered
                collapse-mode="width"
                :collapsed-width="64"
                :width="180"
                :collapsed="collapsed"
                class="h-full"
            >
                <n-scrollbar class="h-full">
                    <n-menu
                        :collapsed-width="64"
                        :collapsed="collapsed"
                        :collapsed-icon-size="22"
                        :value="route.name"
                        :options="menuOptions"
                    />
                </n-scrollbar>
            </n-layout-sider>
            <n-layout-content>
                <div class="mx-8 w-auto lg:mx-auto lg:w-[60vw] my-8">
                    <router-view />
                </div>
            </n-layout-content>
        </n-layout>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>

<style scoped>
.admin-container {
    height: calc(100vh - 7rem);
}
</style>
