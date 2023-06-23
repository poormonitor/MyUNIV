import { createDiscreteApi, useDialog } from "naive-ui";
import { useRouter } from "vue-router";

const { message } = createDiscreteApi(["message"]);

const paramsError = async () => {
    const router = useRouter();
    const dialog = useDialog();
    dialog.error({
        title: "错误",
        content: "请求参数有误。",
        positiveText: "回到首页",
        onPositiveClick: () => {
            router.push({ name: "home" });
        },
    });
    return new Promise(() => {});
};

export { message, paramsError };
