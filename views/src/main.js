import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";
import WebFont from "webfontloader";
import { AxiosPlugin } from "./axios";

import App from "./App.vue";
import "./assets/index.css";
import router from "./router";

const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(AxiosPlugin);
app.use(router);

const meta = document.createElement("meta");
meta.name = "naive-ui-style";
document.head.appendChild(meta);

app.mount("#app");

WebFont.load({
    google: {
        families: ["Inter:500,800", "Noto Sans SC:500,800"],
    },
});
