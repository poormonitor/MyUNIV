<script setup>
const axios = inject("axios");
const props = defineProps(["show", "year", "yearOptions"]);
const emits = defineEmits(["update:show", "rank"]);
const score = ref(600);
const year = ref(props.year);

const visible = computed({
    get() {
        year.value = props.year;
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const handleQueryKeyUp = (event) => {
    if (event.key === "Enter") fetchRank();
};

const fetchRank = () => {
    axios
        .get("/get/score", { params: { score: score.value, year: year.value } })
        .then((response) => {
            if (response.data) {
                emits("rank", response.data.rank);
                visible.value = false;
            }
        });
};
</script>

<template>
    <n-modal
        v-model:show="visible"
        title="分数转换"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="fetchRank"
    >
        <n-form class="px-8 pt-8">
            <n-form-item label="年份">
                <n-select
                    v-model:value="year"
                    :options="props.yearOptions"
                ></n-select>
            </n-form-item>
            <n-form-item label="分数">
                <n-input-number
                    class="w-full"
                    @keyup="handleQueryKeyUp"
                    v-model:value="score"
                ></n-input-number>
            </n-form-item>
        </n-form>
    </n-modal>
</template>
