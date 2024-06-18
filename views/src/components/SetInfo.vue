<script setup>
import { useInfoStore } from "../stores/info";
import { majors } from "../const";

const props = defineProps(["year", "yearOptions"]);
const emits = defineEmits(["finish"]);
const infoStore = useInfoStore();
const show = ref(false);
const rankShow = ref(false);

const infoSet = reactive({
    rank: infoStore.rank,
    must: infoStore.must,
    disabled: infoStore.disabled,
});

const must_options = majors.slice(1).map((item, index) => ({
    label: item,
    value: index + 1,
}));

const setRank = (rank) => {
    infoSet.rank = rank;
};

const open = () => {
    show.value = true;
};

watch(show, (value) => {
    if (value) {
        infoSet.rank = infoStore.rank;
        infoSet.must = infoStore.must;
        infoSet.disabled = infoStore.disabled;
    }
});

const submitRequest = () => {
    infoStore.rank = infoSet.rank;
    infoSet.must.sort((a, b) => a - b);
    infoStore.must = infoSet.must;
    infoStore.disabled = infoSet.disabled;
    show.value = false;
    emits("finish", infoSet.rank, infoSet.must);
};

defineExpose({
    open,
});
</script>

<template>
    <n-float-button
        class="z-10"
        @click="show = true"
        :right="25"
        :top="80"
        width="auto"
        shape="square"
    >
        <template #description>
            <div class="mx-1" v-if="infoStore.setted">
                <div v-if="infoStore.rank">{{ infoStore.rank }}</div>
                <div v-if="infoStore.must.length" class="whitespace-nowrap">
                    {{ infoStore.display }}
                </div>
            </div>
            <div class="mx-1" v-else>修改信息</div>
        </template>
    </n-float-button>
    <GetRank
        v-model:show="rankShow"
        :year="props.year"
        :yearOptions="props.yearOptions"
        @rank="setRank"
    />
    <n-modal
        v-model:show="show"
        title="修改个人信息"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="submitRequest"
    >
        <div class="mx-5 mt-8">
            <n-form :model="infoSet" ref="form">
                <n-form-item label="位次号">
                    <div class="flex gap-x-2 w-full">
                        <n-input-number
                            class="flex-grow"
                            v-model:value="infoSet.rank"
                        ></n-input-number>
                        <n-button @click="rankShow = true"> 转换 </n-button>
                    </div>
                </n-form-item>
                <n-form-item label="选考科目">
                    <n-checkbox-group :max="3" v-model:value="infoSet.must">
                        <n-space item-style="display: flex;">
                            <n-checkbox
                                v-for="option in must_options"
                                :value="option.value"
                                :label="option.label"
                            />
                        </n-space>
                    </n-checkbox-group>
                </n-form-item>
                <n-form-item label="不再提示">
                    <n-switch v-model:value="infoSet.disabled" />
                </n-form-item>
            </n-form>
        </div>
    </n-modal>
</template>
