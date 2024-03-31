import { VueQueryPlugin } from "@tanstack/vue-query";
import "./assets/main.css";
import VueFormulate from "@braid/vue-formulate";

import { createApp } from "vue";
import App from "./App.vue";

createApp(App).use(VueQueryPlugin).mount("#app");
