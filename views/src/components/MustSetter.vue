<script setup>
import { message } from "../discrete";
import { useUserStore } from "../stores/user";
import { majors } from "../const";

const axios = inject("axios");
const props = defineProps(["show"]);
const emits = defineEmits(["update:show"]);
const form = ref(null);
const userStore = useUserStore();
const visible = computed({
    get() {
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const mustSet = ref(userStore.must);

const submitRequest = () => {
    axios
        .post("/user/must", {
            must: mustSet.value,
        })
        .then((respoelse) => {
            if (respoelse.data.result == "success") {
                visible.value = false;
                message.success("科目修改成功");
            }
        });
};

const must_options = majors.slice(1).map((item, index) => ({
    label: item,
    value: index + 1,
}));
</script>

<template>
    <n-modal
        v-model:show="visible"
        title="修改选考科目"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="submitRequest"
    >
        <n-form ref="form">
            <div class="mx-8 mb-6 mt-10">
                <n-form-item label="选考科目">
                    <n-checkbox-group
                        class="mt-4"
                        :max="3"
                        v-model:value="mustSet"
                    >
                        <n-space item-style="display: flex;">
                            <n-checkbox
                                v-for="option in must_options"
                                :value="option.value"
                                :label="option.label"
                            />
                        </n-space>
                    </n-checkbox-group>
                </n-form-item>
            </div>
        </n-form>
    </n-modal>
</template>
