<script setup lang="jsx">
import { NIcon } from "naive-ui";
import { useRoute, RouterLink } from "vue-router";
import { School, AppsOutline,Archive } from "@vicons/ionicons5";
import UserPanel from "./UserPanel.vue";

const route = useRoute();

const collapsed = inject("collapsed");
const showSideBar = ref(false);

const renderLabel = (icon, target, label) => {
    return () => (
        <div class="flex items-center gap-x-1.5">
            <NIcon size="0.9rem">{() => h(icon)}</NIcon>
            <RouterLink class="text-[0.9rem]" to={{ name: target }}>
                {label}
            </RouterLink>
        </div>
    );
};

const menuOptions = [
    {
        label: renderLabel(School, "query", "搜专业"),
        key: "query",
    },
    {
        label: renderLabel(Archive, "my", "备选专业"),
        key: "my",
    },
];
</script>

<template>
    <n-drawer
        v-model:show="showSideBar"
        placement="left"
        width="180px"
        v-if="collapsed"
    >
        <n-menu
            :value="route.name"
            @update:value="showSideBar = false"
            :options="menuOptions"
        />
    </n-drawer>
    <div class="h-14 flex items-center" id="main-header">
        <div class="pl-3">
            <n-button
                @click="showSideBar = true"
                size="small"
                quaternary
                v-if="collapsed"
            >
                <n-icon size="1rem"><AppsOutline /></n-icon>
            </n-button>
        </div>
        <div class="pl-3 select-none flex items-baseline">
            <router-link
                :to="{ name: 'home' }"
                class="font-sans text-2xl font-bold gradient-title from-cyan-500 via-sky-600 to-blue-800"
            >
                MyUNIV
            </router-link>
        </div>
        <n-menu
            class="pl-3"
            :value="route.name"
            v-if="!collapsed"
            mode="horizontal"
            :options="menuOptions"
        />
        <div class="flex grow justify-end pr-6 md:pr-10">
            <UserPanel v-if="route.name !== 'login'" />
        </div>
    </div>
</template>
