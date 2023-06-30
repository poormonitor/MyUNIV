import { createRouter, createWebHashHistory } from "vue-router";
import { useUserStore } from "../stores/user";
import { useMyStore } from "../stores/my";
import { message } from "../discrete";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            name: "index",
            redirect: { name: "home" },
            component: () => import("../views/Index.vue"),
            meta: {
                requiresAuth: false,
                requiresAdmin: false,
            },
            children: [
                {
                    path: "",
                    name: "home",
                    component: () => import("../views/Home.vue"),
                    meta: {
                        title: "首页",
                    },
                },
                {
                    path: "query",
                    name: "query",
                    component: () => import("../views/Query.vue"),
                    meta: {
                        title: "查询",
                    },
                },
                {
                    path: "my",
                    name: "my",
                    component: () => import("../views/My.vue"),
                    meta: {
                        title: "备选",
                    },
                },
                {
                    path: "login",
                    name: "login",
                    component: () => import("../views/Login.vue"),
                    meta: {
                        title: "用户登录",
                    },
                },
                {
                    path: "view",
                    name: "view",
                    redirect: { name: "home" },
                    component: () => import("../views/View.vue"),
                    children: [
                        {
                            path: "univ/:sid",
                            name: "univ",
                            component: () => import("../views/Univ.vue"),
                            meta: {
                                title: "学校",
                            },
                        },
                        {
                            path: "major/:mid",
                            name: "major",
                            component: () => import("../views/Major.vue"),
                            meta: {
                                title: "专业",
                            },
                        },
                    ],
                },
            ],
        },
        {
            path: "/admin",
            name: "admin",
            redirect: { name: "user" },
            component: () => import("../views/Admin.vue"),
            meta: {
                requiresAuth: true,
                requiresAdmin: false,
            },
            children: [
                {
                    path: "user",
                    name: "user",
                    component: () => import("../views/User.vue"),
                    meta: {
                        title: "用户管理",
                        requiresAdmin: true,
                    },
                },
                {
                    path: "upload",
                    name: "upload",
                    component: () => import("../views/Upload.vue"),
                    meta: {
                        title: "数据上传",
                    },
                },
                {
                    path: "tag",
                    name: "tag",
                    component: () => import("../views/Tag.vue"),
                    meta: {
                        title: "添加标签",
                    },
                },
            ],
        },
        {
            path: "/:pathMatch(.*)*",
            name: "lost",
            component: () => import("../views/NotFound.vue"),
        },
    ],
});

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title + " - MyUNIV";
    }
    const userStore = useUserStore();
    const myStore = useMyStore();

    if (
        to.meta.requiresAuth &&
        userStore.uid &&
        userStore.expires <= new Date().getTime()
    ) {
        message.info("登录过期，请重新登录");
        userStore.logout();
        myStore.reset();
        return { name: "login" };
    }
    if (to.meta.requiresAuth && !userStore.uid) {
        message.info("请先登录");
        return { name: "login" };
    }
    if (to.meta.requiresAdmin && !userStore.admin) {
        message.error("需要管理员权限");
        return { name: "home" };
    }
    if (userStore.uid && ["login", "reg"].includes(to.name))
        return { name: "home" };
});

export default router;
