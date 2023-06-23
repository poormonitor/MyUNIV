import { createRouter, createWebHashHistory } from "vue-router";
import { useUserStore } from "../stores/user";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/:pathMatch(.*)*",
            name: "lost",
            component: () => import("../views/NotFound.vue"),
        },
    ],
});

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title + " - MyEXAM";
    }
    const userStore = useUserStore();

    if (
        to.meta.requiresAuth &&
        userStore.uid &&
        userStore.expires <= new Date().getTime()
    ) {
        userStore.logout();
        return { name: "login" };
    }
    if (to.meta.requiresAuth && !userStore.uid) return { name: "login" };
    if (to.meta.requiresAdmin && !userStore.admin) return { name: "home" };
    if (userStore.uid && ["login", "reg"].includes(to.name))
        return { name: "home" };
});

export default router;
