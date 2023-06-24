import { ref } from "vue";
import { defineStore } from "pinia";

export const useMyStore = defineStore(
    "my",
    () => {
        const my = ref([]);

        function reset() {
            my.value = [];
        }

        function add(id) {
            my.value.push(id);
        }

        function t_add(id) {
            return my.value.concat([id]);
        }

        function t_remove(id) {
            return my.value.filter((item) => item != id);
        }

        function remove(id) {
            my.value = my.value.filter((item) => item != id);
        }

        function has(id) {
            return my.value.includes(id);
        }

        return { my, add, remove, has, reset, t_add, t_remove };
    },
    {
        persist: {
            storage: sessionStorage,
        },
    }
);
