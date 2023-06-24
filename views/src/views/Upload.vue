<script setup>
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { message } from "../discrete";

const axios = inject("axios");
const fileList = ref([]);
const time = ref(new Date().getTime());

const upload = () => {
    if (!fileList.value) return message.error("请先选择文件");
    const formData = new FormData();
    formData.append("file", fileList.value[0].file);
    formData.append("year", new Date(time.value).getFullYear());
    axios.post("/manage/data", formData).then((response) => {
        if (response.data.result == "success") {
            fileList.value = [];
            message.success("开始处理");
        }
    });
};

const conn = () => {
    axios.post("/manage/conn").then((response) => {
        if (response.data.result == "success") {
            message.success("开始处理");
        }
    });
};

const clean = () => {
    axios.post("/manage/clean").then((response) => {
        if (response.data.result == "success") {
            message.success("清空成功");
        }
    });
};
</script>
<template>
    <p class="text-xl md:text-3xl font-bold pb-4 pt-2">上传数据</p>
    <div class="mt-2 mb-4">
        <p>
            请从浙江省教育考试院下载发布的投档数据，格式为xlsx，并上传到本系统。
        </p>
        <p>投档数据：学校代号 学校名称 专业代号 专业名称 计划数 分数线 位次</p>
        <p>
            选课数据：省份 院校名称 专业（类）名称 类中所含专业 层次
            选考科目要求
        </p>
        <p>系统自动检测数据类型。</p>
    </div>

    <n-form>
        <n-form-item label="数据年份">
            <n-date-picker v-model:value="time" type="year" />
        </n-form-item>
        <n-form-item label="上传文件">
            <n-upload
                accept=".xlsx, .xls"
                v-model:file-list="fileList"
                :max="1"
            >
                <n-upload-dragger>
                    <div style="margin-bottom: 12px">
                        <n-icon size="48" :depth="3">
                            <archive-icon />
                        </n-icon>
                    </div>
                    <n-text style="font-size: 16px">
                        点击或者拖动文件到该区域来上传
                    </n-text>
                    <n-p depth="3" style="margin: 8px 0 0 0">
                        请不要上传敏感数据，比如你的银行卡号和密码，信用卡号有效期和安全码
                    </n-p>
                </n-upload-dragger>
            </n-upload>
        </n-form-item>
    </n-form>
    <div class="flex justify-center">
        <div class="w-64 flex flex-col gap-y-4">
            <div class="flex flex-col">
                <n-button type="success" :block="true" @click="upload">
                    上传
                </n-button>
            </div>
            <div class="flex gap-x-4">
                <div class="basis-1/2">
                    <n-button type="info" :block="true" @click="conn">
                        链接数据
                    </n-button>
                </div>
                <div class="basis-1/2">
                    <n-popconfirm @positive-click="clean">
                        <template #trigger>
                            <n-button type="error" :block="true">
                                清空数据
                            </n-button>
                        </template>
                        确认删除？
                    </n-popconfirm>
                </div>
            </div>
        </div>
    </div>
</template>
