<template>
    <n-layout class="min-h-full pb-12">
        <n-layout-header bordered>
            <Header></Header>
        </n-layout-header>
        <n-layout-content>
            <router-view v-slot="{ Component }">
                <keep-alive :include="['Query', 'My']">
                    <component :is="Component" />
                </keep-alive>
            </router-view>
        </n-layout-content>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>
