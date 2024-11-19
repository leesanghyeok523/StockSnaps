<template>
  <header class="header-nav">
    <nav>
      <ul class="menu">
        <li><router-link to="/" exact>Home</router-link></li>
        <li v-if="authStore.isAuthenticated">
          <router-link to="/profile">Profile</router-link>
        </li>
        <li v-else @click="navigateToLogin" class="disabled">Profile</li>
      </ul>
    </nav>
  </header>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  setup() {
    const authStore = useAuthStore();

    const navigateToLogin = () => {
      window.location.href = '/login'; // 로그인 페이지로 이동
    };

    return { authStore, navigateToLogin };
  },
};
</script>

<style scoped>
.menu li a.router-link-active {
  color: #007aff;
  font-weight: bold;
  border-bottom: 2px solid #007aff;
}

.menu li.disabled {
  color: #999;
  cursor: not-allowed;
}
</style>










