<script setup>
import { message } from "../discrete";
import md5 from "crypto-js/md5";

const axios = inject("axios");
const props = defineProps(["show", "uid"]);
const emits = defineEmits(["update:show"]);
const form = ref(null);
const visible = computed({
    get() {
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const passwdSet = reactive({
    new: "",
});

const rules = {
    new: [
        {
            required: true,
            validator: (rule, value) => {
                return /^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$/.test(value);
            },
            message: "密码应该同时包括字母、数字，且长6-20字符",
            trigger: ["input", "blur"],
        },
    ],
};

const submitRequest = () => {
    form.value
        .validate()
        .catch((error) => {})
        .then(() => {
            axios
                .post("/users/passwd", {
                    uid: props.uid,
                    passwd: md5(passwdSet.new).toString(),
                })
                .then((respoelse) => {
                    if (respoelse.data.result == "success") {
                        visible.value = false;
                        message.success("密码修改成功。");
                    }
                });
        });
};
</script>

<template>
    <n-modal
        v-model:show="visible"
        title="修改用户密码"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="submitRequest"
    >
        <n-form :rules="rules" :model="passwdSet" ref="form">
            <div class="mx-8 mb-6 mt-10">
                <n-form-item label="新密码" path="new">
                    <n-input
                        placeholder="新密码"
                        v-model:value="passwdSet.new"
                        type="password"
                        :input-props="{ autocomplete: 'off' }"
                    >
                    </n-input>
                </n-form-item>
            </div>
        </n-form>
    </n-modal>
</template>