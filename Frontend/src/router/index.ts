import { createRouter, createWebHistory } from "vue-router";
import UserView from "@/views/UsersView.vue";
import TeamsView from "@/views/TeamsView.vue";
import CouponsView from "@/views/CouponsView.vue";
import ReviewsView from "@/views/ReviewsView.vue";

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
  ],
});

export default router;
