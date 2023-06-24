import { ref } from "vue";
import { defineStore } from "pinia";

export const useUserStore = defineStore(
    "user",
    () => {
        const uid = ref(null);
        const name = ref(null);
        const access_token = ref(null);
        const admin = ref(false);
        const must = ref([]);
        const expires = ref(new Date().getTime());

        function login(
            user_access_token,
            user_uid,
            user_name,
            user_admin,
            user_expires,
            user_must
        ) {
            access_token.value = user_access_token;
            uid.value = user_uid;
            name.value = user_name;
            admin.value = user_admin;
            expires.value = user_expires;
            must.value = user_must;
        }

        function logout() {
            uid.value = null;
            name.value = null;
            admin.value = false;
            access_token.value = null;
            expires.value = new Date().getTime();
        }

        return { uid, access_token, admin, name, expires, must, login, logout };
    },
    {
        persist: {
            storage: sessionStorage,
        },
    }
);
