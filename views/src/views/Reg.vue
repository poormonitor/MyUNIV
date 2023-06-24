<script setup>
import { useRouter } from "vue-router";
import md5 from "crypto-js/md5";
import { message } from "../discrete";
import { majors } from "../const";

const router = useRouter();
const axios = inject("axios");
const form = ref(null);

const regForm = reactive({
    uid: "",
    name: "",
    passwd: "",
    repeat: "",
    must: [],
});

const submitReg = () => {
    form.value
        .validate()
        .catch((error) => {})
        .then(() => {
            axios
                .post("/user/reg", {
                    uid: regForm.uid,
                    name: regForm.name,
                    passwd: md5(regForm.passwd).toString(),
                    must: regForm.must,
                })
                .then((response) => {
                    if (response.data.result === "success") {
                        message.success("注册成功。");
                        router.push({ name: "login" });
                    }
                });
        });
};

const rules = {
    uid: [
        {
            required: true,
            message: "用户名只能包含数字和字母，且长度在3-10内",
            validator: (rule, value) => {
                return /^[a-zA-Z0-9]{3,10}$/.test(value);
            },
            trigger: ["input", "blur"],
        },
    ],
    name: [
        {
            required: true,
            message: "请输入姓名",
            trigger: ["input", "blur"],
        },
    ],
    must: [
        {
            required: true,
            validator: (rule, value) => {
                return value.length === 3;
            },
            message: "应该选择三个选考科目",
            trigger: ["input", "blur"],
        },
    ],
    passwd: [
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
            validator: (rule, value) => value === regForm.passwd,
            message: "两次输入的密码不一致",
            trigger: ["input", "blur"],
        },
    ],
};

const must_options = majors.slice(1).map((item, index) => ({
    label: item,
    value: index + 1,
}));
</script>

<template>
    <div class="mx-8 w-auto md:mx-auto md:w-[60vw] lg:w-[40vw] my-12">
        <div class="border px-8 md:px-20 py-12 rounded-2xl">
            <p class="text-lg text-indigo-600 mb-2">欢迎使用 MyUNIV</p>
            <p class="text-4xl font-bold">注册</p>
            <n-form
                ref="form"
                size="large"
                class="mt-10 flex flex-col gap-y-4"
                :model="regForm"
                :rules="rules"
            >
                <n-form-item label="用户名" path="uid">
                    <n-input
                        :input-props="{ autocomplete: 'username' }"
                        v-model:value="regForm.uid"
                    ></n-input>
                </n-form-item>
                <n-form-item label="姓名" path="name">
                    <n-input
                        :input-props="{ autocomplete: 'nick' }"
                        v-model:value="regForm.name"
                    ></n-input>
                </n-form-item>
                <n-form-item label="选考科目" path="must">
                    <n-checkbox-group :max="3" v-model:value="regForm.must">
                        <n-space item-style="display: flex;">
                            <n-checkbox
                                v-for="option in must_options"
                                :value="option.value"
                                :label="option.label"
                            />
                        </n-space>
                    </n-checkbox-group>
                </n-form-item>
                <n-form-item label="密码" path="passwd">
                    <n-input
                        :input-props="{ autocomplete: 'new-password' }"
                        type="password"
                        v-model:value="regForm.passwd"
                    ></n-input>
                </n-form-item>
                <n-form-item label="重复密码" path="repeat">
                    <n-input
                        :input-props="{ autocomplete: 'new-password' }"
                        type="password"
                        v-model:value="regForm.repeat"
                    ></n-input>
                </n-form-item>
                <div class="flex justify-center">
                    <span>
                        已有账号？去
                        <router-link
                            class="text-blue-500 hover:text-blue-700"
                            :to="{ name: 'login' }"
                        >
                            登录
                        </router-link>
                    </span>
                </div>
                <div class="flex gap-x-4 justify-center mt-4">
                    <n-button
                        class="basis-1/2"
                        type="primary"
                        @click="submitReg"
                        >注册</n-button
                    >
                </div>
            </n-form>
        </div>
    </div>
</template>
