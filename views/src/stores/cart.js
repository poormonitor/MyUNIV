import { ref } from "vue";
import { defineStore } from "pinia";
import { axios } from "../axios";
import { useUserStore } from "./user";

const userStore = useUserStore();

export const useCartStore = defineStore(
    "cart",
    () => {
        const cart = ref([]);

        function fetch() {
            if (userStore.uid) {
                axios.get("/user/cart").then((response) => {
                    if (response.data.list) cart.value = response.data.list;
                });
            }
        }

        function update() {
            if (userStore.uid) {
                axios.post("/user/cart", { cart: cart.value });
            }
        }

        function add(pid) {
            cart.value.push(pid);
            update();
        }

        function del(fid) {
            cart.value = cart.value.filter((item) => item !== fid);
            update();
        }

        function has(fid) {
            return cart.value.includes(fid);
        }

        function reset() {
            cart.value = [];
        }

        return { cart, add, del, has, reset, update, fetch };
    },
    {
        persist: {
            storage: localStorage,
        },
    }
);
