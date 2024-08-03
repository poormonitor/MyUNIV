<script setup></script>

<template>
    <div class="mx-8 w-auto md:mx-auto md:w-[70vw] lg:w-[60vw] my-8 md:my-10">
        <router-view v-slot="{ Component }">
            <Suspense :key="Component">
                <component :is="Component" />
                <template #fallback>
                    <div class="flex place-content-center mt-[40vh]">
                        <n-spin>
                            <template #description> 加载中 </template>
                        </n-spin>
                    </div>
                </template>
            </Suspense>
        </router-view>
    </div>
</template>
