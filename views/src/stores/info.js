import { ref } from "vue";
import { defineStore } from "pinia";
import { majors_short } from "../const";

export const useInfoStore = defineStore(
    "info",
    () => {
        const agree = ref(false);
        const must = ref([]);
        const rank = ref(null);
        const disabled = ref(false);

        const setted = computed(() => {
            return must.value.length > 0 || rank.value !== null;
        });
        const display = computed(() => {
            if (!must.value) {
                return "";
            }

            let now = String(must.value);
            let ans = [];
            for (let i = 0; i < now.length; i++) {
                ans.push(majors_short[Number(now[i])]);
            }
            return ans.join("");
        });

        return { agree, must, rank, disabled, setted, display };
    },
    {
        persist: {
            storage: localStorage,
        },
    }
);
