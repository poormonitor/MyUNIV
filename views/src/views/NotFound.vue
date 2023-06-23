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
            <n-result
                class="mt-20"
                status="404"
                title="404 资源不存在"
                description="生活总归带点荒谬"
            >
                <template #footer>
                    <n-button @click="router.push({ name: 'home' })">
                        回到首页
                    </n-button>
                </template>
            </n-result>
        </n-layout-content>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>