<script setup>
import Card from "./Card.vue";
</script>

<template>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-x-3 gap-y-4">
        <Card title="易用">
            <template #content>
                前端逻辑清晰，操作提示直观，无需教学也可使用，极大的降低了学校专业查询成本。
            </template>
        </Card>
        <Card title="智能">
            <template #content>
                多种条件筛选符合要求的学校和专业，并可以根据相关要求自动筛选备选志愿供参考。
            </template>
        </Card>
        <Card title="全面">
            <template #content>
                历年数据一网打尽，不再需要多处访问、下载，一站式获得专业信息数据。
            </template>
        </Card>
    </div>
</template>
