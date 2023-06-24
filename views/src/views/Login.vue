<script setup>
import md5 from "crypto-js/md5";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import { useMyStore } from "../stores/my";

const userStore = useUserStore();
const myStore = useMyStore();
const router = useRouter();
const axios = inject("axios");

const loginForm = reactive({
    uid: "",
    passwd: "",
});

const submitLogin = () => {
    axios
        .post("/user/login", {
            uid: loginForm.uid,
            passwd: md5(loginForm.passwd).toString(),
        })
        .then(async (response) => {
            if (response.data.access_token) {
                let token = response.data.access_token;
                let payload = JSON.parse(atob(token.split(".")[1]));
                userStore.login(
                    token,
                    payload.uid,
                    payload.name,
                    payload.admin,
                    payload.exp * 1000,
                    payload.must
                );
                axios.get("/user/major").then((response) => {
                    if (response.data) myStore.my = response.data;
                });
                router.push({ name: "home" });
            }
        });
};
</script>

<template>
    <div class="mx-8 w-auto md:mx-auto md:w-[60vw] lg:w-[40vw] my-20">
        <div class="border px-8 md:px-20 py-12 rounded-2xl">
            <p class="text-lg text-indigo-600 mb-2">欢迎使用 MyUNIV</p>
            <p class="text-4xl font-bold">登录</p>
            <n-form size="large" class="mt-10">
                <n-form-item label="用户名">
                    <n-input
                        :input-props="{ autocomplete: 'username' }"
                        v-model:value="loginForm.uid"
                    ></n-input>
                </n-form-item>
                <n-form-item label="密码">
                    <n-input
                        :input-props="{ autocomplete: 'current-password' }"
                        type="password"
                        v-model:value="loginForm.passwd"
                    ></n-input>
                </n-form-item>
                <div class="flex justify-center">
                    <span>
                        没有账号？去
                        <router-link
                            class="text-blue-500 hover:text-blue-700"
                            :to="{ name: 'reg' }"
                        >
                            注册
                        </router-link>
                    </span>
                </div>
                <div class="flex gap-x-4 justify-center mt-4">
                    <n-button
                        class="basis-1/2"
                        type="primary"
                        @click="submitLogin"
                    >
                        登录
                    </n-button>
                </div>
            </n-form>
        </div>
    </div>
</template>
