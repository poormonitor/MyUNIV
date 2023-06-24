<script setup>
import { message } from "../discrete";

const axios = inject("axios");
const data = reactive({ tag: "", school: "" });

const submit = () => {
    axios.post("/manage/tag", data).then((response) => {
        if (response.data.result == "success") {
            data.school = "";
            message.success("添加成功");
        }
    });
};
</script>
<template>
    <p class="text-xl md:text-3xl font-bold pb-4 pt-2">添加标签</p>
    <div class="mt-2 mb-4">
        <p>
            在学校框中输入学校名称，换行分割，每行一个学校。
            在标签栏中输入需要加入的标签。
        </p>
    </div>

    <n-form>
        <n-form-item label="标签名称">
            <n-input v-model:value="data.tag" />
        </n-form-item>
        <n-form-item label="上传文件">
            <n-input
                v-model:value="data.school"
                class="h-48"
                type="textarea"
                placeholder="学校列表，换行分割"
            />
        </n-form-item>
    </n-form>
    <div class="flex justify-center">
        <div class="w-32">
            <n-button type="success" :block="true" @click="submit"
                >添加</n-button
            >
        </div>
    </div>
</template>
