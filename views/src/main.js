import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";
import { AxiosPlugin } from "./axios";

import App from "./App.vue";
import "./assets/index.css";
import router from "./router";

const app = createApp(App);
app.use(AxiosPlugin);
app.use(router);

const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);
app.use(pinia);

const meta = document.createElement("meta");
meta.name = "naive-ui-style";
document.head.appendChild(meta);

app.mount("#app");
