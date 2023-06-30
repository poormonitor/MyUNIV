import { ref, watch, computed } from "vue";
import { defineStore } from "pinia";
import { message } from "../discrete";

export const useMyStore = defineStore(
    "my",
    () => {
        const my = ref([[]]);
        const order = ref(0);

        function reset() {
            my.value[order.value] = [];
        }

        function add(id) {
            if (my.value[order.value].length >= 200) {
                message.error("项目过多");
            } else {
                my.value[order.value].push(id);
            }
        }

        function remove(id) {
            my.value[order.value] = my.value[order.value].filter(
                (item) => item != id
            );
        }

        const count = computed(() => my.value[order.value].length);

        function has(id) {
            return my.value[order.value].includes(id);
        }

        function get() {
            return my.value[order.value];
        }

        function removeList() {
            my.value.splice(order.value, 1);
            order.value -= 1;
        }

        const newList = computed(() => my.value.length);

        watch(order, (val) => {
            if (val === "new") {
                order.value = my.value.length;
                my.value[order.value] = [];
            }
        });

        return {
            my,
            order,
            add,
            remove,
            get,
            count,
            has,
            reset,
            newList,
            removeList,
        };
    },
    {
        persist: {
            storage: sessionStorage,
        },
    }
);
