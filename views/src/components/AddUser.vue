<script setup>
import { message } from "../discrete";
import md5 from "crypto-js/md5";

const axios = inject("axios");
const props = defineProps(["show", "uid"]);
const emits = defineEmits(["update:show", "finish"]);
const form = ref(null);
const visible = computed({
    get() {
        return props.show;
    },
    set(value) {
        emits("update:show", value);
    },
});

const newUser = reactive({
    passwd: "",
    name: "",
    uid: "",
});

const rules = {
    uid: [
        {
            required: true,
            message: "用户名只能包含数字和字母，且长度在3-10内",
            validator: (rule, value) => {
                return /^[a-zA-Z0-9]{3,10}$/.test(value);
            },
            trigger: ["input", "blur"],
        },
    ],
    name: [
        {
            required: true,
            message: "请输入姓名",
            trigger: ["input", "blur"],
        },
    ],
    name: [
        {
            required: true,
            message: "请输入密码",
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
                .post("/users/new", {
                    uid: newUser.uid,
                    name: newUser.name,
                    passwd: md5(newUser.passwd).toString(),
                })
                .then((respoelse) => {
                    if (respoelse.data.result == "success") {
                        visible.value = false;
                        emits("finish");
                        message.success("用户添加成功");
                    }
                });
        });
};
</script>

<template>
    <n-modal
        v-model:show="visible"
        title="添加用户"
        preset="dialog"
        positive-text="确认"
        negative-text="取消"
        class="w-4/5 md:3/5 lg:w-2/5"
        @positive-click="submitRequest"
    >
        <n-form :rules="rules" :model="newUser" ref="form">
            <div class="mx-8 mb-6 mt-10">
                <n-form-item label="用户名" path="uid">
                    <n-input
                        placeholder="用户名"
                        v-model:value="newUser.uid"
                        :input-props="{ autocomplete: 'off' }"
                    >
                    </n-input>
                </n-form-item>
                <n-form-item label="姓名" path="name">
                    <n-input
                        placeholder="姓名"
                        v-model:value="newUser.name"
                        :input-props="{ autocomplete: 'off' }"
                    >
                    </n-input>
                </n-form-item>
                <n-form-item label="密码" path="passwd">
                    <n-input
                        placeholder="密码"
                        v-model:value="newUser.passwd"
                        type="password"
                        :input-props="{ autocomplete: 'off' }"
                    >
                    </n-input>
                </n-form-item>
            </div>
        </n-form>
    </n-modal>
</template>
