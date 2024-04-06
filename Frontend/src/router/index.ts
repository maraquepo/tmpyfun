import { createRouter, createWebHistory } from "vue-router";
import UserView from "@/views/UsersView.vue";
import TeamsView from "@/views/TeamsView.vue";
import CouponsView from "@/views/CouponsView.vue";
import ReviewsView from "@/views/ReviewsView.vue";
import ScriptsView from "@/views/ScriptsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "users",
      component: UserView,
    },
    {
      path: "/teams",
      name: "teams",
      component: TeamsView,
    },
    {
      path: "/coupons",
      name: "coupons",
      component: CouponsView,
    },
    {
      path: "/reviews",
      name: "reviews",
      component: ReviewsView,
    },
    {
      path: "/scripts",
      name: "scripts",
      component: ScriptsView,
    },
  ],
});

export default router;
