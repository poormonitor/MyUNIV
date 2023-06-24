<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>
<template>
    <n-layout class="min-h-full pb-12">
        <n-layout-header bordered>
            <Header></Header>
        </n-layout-header>
        <n-layout-content>
            <router-view v-slot="{ Component }">
                <keep-alive>
                    <component :is="Component" />
                </keep-alive>
            </router-view>
        </n-layout-content>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>
