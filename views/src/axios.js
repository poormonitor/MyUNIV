import ax from "axios";
import { message } from "./discrete";
import { useUserStore } from "./stores/user";
import { useMyStore } from "./stores/my";
import router from "./router/index";

const instance = ax.create({
    baseURL: "/api",
    timeout: 5000,
});

instance.interceptors.request.use(
    (config) => {
        const userStore = useUserStore();
        const myStore = useMyStore();

        let access_token = userStore.access_token;

        if (access_token) {
            if (userStore.expires <= new Date().getTime()) {
                userStore.logout();
                myStore.reset();
            } else {
                config.headers.Authorization = "Bearer " + access_token;
            }
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            const userStore = useUserStore();
            const myStore = useMyStore();

            userStore.logout();
            myStore.reset();
            message.info("登录失效，请重新登录。");
            router.push({ name: "login" });
        } else if (typeof error.response?.data?.detail === "string") {
            message.error(error.response.data.detail);
        } else {
            message.error(error.message);
        }
        return Promise.reject(error);
    }
);

export const AxiosPlugin = {
    install: (app) => {
        app.provide("axios", instance);
    },
};

export const axios = instance;
