import { VueQueryPlugin } from "@tanstack/vue-query";
import "./assets/main.css";
import VueFormulate from "@braid/vue-formulate";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

createApp(App).use(VueQueryPlugin).use(router).mount("#app");
