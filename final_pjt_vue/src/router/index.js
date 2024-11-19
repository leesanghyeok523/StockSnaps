import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import SignupPage from '../views/SignupPage.vue';
import MapPage from '../views/MapPage.vue';
import SavingsComparisonPage from '../views/SavingsComparisonPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import ExchangeRates from '@/views/ExchangeRates.vue';
import CommunityPosts from '@/views/CommunityPosts.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/map', component: MapPage, meta: { requiresAuth: true } },
  { path: '/savings-comparison', component: SavingsComparisonPage, meta: { requiresAuth: true } },
  { path: '/profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/exchange-rates', component: ExchangeRates, meta: { requiresAuth: true } }, // 추가된 경로
  { path: '/community-posts', component: CommunityPosts, meta: { requiresAuth: true } }, // 추가된 경로
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 라우터 가드
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
