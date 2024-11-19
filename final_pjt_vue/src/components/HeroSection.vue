<template>
  <section class="hero-section">
    <div class="bg">
      <!-- 배경 동영상 -->
      <video muted autoplay loop>
        <!-- 동영상 소스 -->
        <source :src="videoSource" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <!-- 텍스트와 버튼 -->
      <div class="text">
        <h1>금융의 모든 것<br />한 곳에서 쉽고 간편하게</h1>
        <p>금융 서비스를 안전하고 쉽게 이용해보세요.</p>
        <div class="buttons">
          <template v-if="!isLoggedIn">
            <button class="action-button" @click="navigateTo('/login')">로그인</button>
            <button class="action-button" @click="navigateTo('/signup')">회원가입</button>
          </template>
          <template v-else>
            <button class="action-button" @click="navigateTo('/map')">맵 데이터</button>
            <button class="action-button" @click="navigateTo('/savings-comparison')">예적금 비교</button>
            <button class="action-button" @click="navigateTo('/exchange-rates')">환율 계산기</button>
            <button class="action-button" @click="navigateTo('/community_posts')">게시판</button>
            <button class="action-button logout-button" @click="handleLogout">로그아웃</button>
          </template>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';
// 동영상 파일 import
import videoFile from '@/assets/background-video.mp4';

export default {
  setup() {
    const authStore = useAuthStore();
    const isLoggedIn = computed(() => authStore.isAuthenticated);

    const navigateTo = (path) => {
      window.location.href = path;
    };

    const handleLogout = () => {
      authStore.logout();
      alert('로그아웃 되었습니다!');
      console.log('로그아웃 성공');
    };

    // 동영상 파일 경로
    const videoSource = videoFile;

    return { isLoggedIn, navigateTo, handleLogout, videoSource };
  },
};
</script>

<style scoped>
/* 전역 여백 제거 */
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

/* 배경 스타일 */
.hero-section {
  width: 100vw; /* Viewport 너비 */
  height: 100vh; /* Viewport 높이 */
  overflow: hidden;
  position: relative;
}

.bg {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 텍스트 및 버튼 레이아웃 */
.text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.text h1 {
  font-size: 3rem;
  font-weight: bold;
  color: black;
  margin-bottom: 20px;
}

.text p {
  font-size: 1.5rem;
  color: black;
  margin-bottom: 40px;
}

.buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

/* 버튼 스타일 */
.action-button {
  padding: 15px 30px;
  font-size: 1.2rem;
  color: white;
  background: rgba(0, 0, 0, 0.7) !important;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.action-button:hover {
  background-color: rgba(0, 0, 0, 0.5) !important;
}

.action-button:active {
  transform: translateY(1px);
}

.logout-button {
  background-color: #ff5252;
}

.logout-button:hover {
  background-color: #ff7979;
}

/* 반응형 스타일 */
@media (max-width: 664px) {
  .text h1 {
    font-size: 2rem;
  }

  .text p {
    font-size: 1rem;
  }
}
</style>


