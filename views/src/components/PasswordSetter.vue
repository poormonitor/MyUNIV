<script setup>
import { message } from "../discrete";
import md5 from "crypto-js/md5";

const axios = inject("axios");
const props = defineProps(["show"]);
const emits = defineEmits(["update:show"]);
const form = ref(null);
const visible = computed({
    get() {
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const passwdSet = reactive({
    old: "",
    new: "",
    repeat: "",
});

const rules = {
    old: [{ required: true }],
    new: [
        {
            required: true,
            validator: (rule, value) => {
                return /^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$/.test(value);
            },
            message: "密码应该同时包括字母、数字，且长6-20字符",
            trigger: ["input", "blur"],
        },
    ],
    repeat: [
        {
            required: true,
            validator: (rule, value) => value === passwdSet.new,
            message: "两次输入的密码不一致",
            trigger: ["input", "blur"],
        },
    ],
};

const submitRequest = () => {
    form.value
        .validate()
        .catch((error) => {})
        .then(() => {
            axios
                .post("/user/passwd", {
                    old: md5(passwdSet.old).toString(),
                    new: md5(passwdSet.new).toString(),
                })
                .then((respoelse) => {
                    if (respoelse.data.result == "success") {
                        visible.value = false;
                        message.success("密码修改成功。");
                    }
                });
        });
};
</script>

<template>
    <n-modal
        v-model:show="visible"
        title="修改密码"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="submitRequest"
    >
        <n-form :rules="rules" :model="passwdSet" ref="form">
            <div class="mx-8 mb-6 mt-10">
                <n-form-item label="原密码" path="old">
                    <n-input
                        placeholder="原密码"
                        v-model:value="passwdSet.old"
                        type="password"
                        :input-props="{ autocomplete: 'current-password' }"
                    >
                    </n-input>
                </n-form-item>
                <n-form-item label="新密码" path="new">
                    <n-input
                        placeholder="新密码"
                        v-model:value="passwdSet.new"
                        type="password"
                        :input-props="{ autocomplete: 'new-password' }"
                    >
                    </n-input>
                </n-form-item>
                <n-form-item label="重复密码" path="repeat">
                    <n-input
                        placeholder="重复密码"
                        v-model:value="passwdSet.repeat"
                        type="password"
                        @enter="submitRequest"
                        :input-props="{ autocomplete: 'new-password' }"
                    >
                    </n-input>
                </n-form-item>
            </div>
        </n-form>
    </n-modal>
</template>