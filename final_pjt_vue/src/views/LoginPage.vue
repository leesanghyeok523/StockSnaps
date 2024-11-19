<template>
  <div class="login-page">
    <div class="login-container">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">아이디</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="아이디를 입력하세요"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>
        <button type="submit" class="login-button">로그인</button>
      </form>
      <button class="back-button" @click="navigateBack">뒤로가기</button>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

export default {
  setup() {
    const authStore = useAuthStore();
    const username = ref('');
    const password = ref('');

    const handleLogin = async () => {
      try {
        await authStore.login(username.value, password.value);
        alert('로그인 성공!');
        console.log('Access Token:', authStore.accessToken);
        console.log('Refresh Token:', authStore.refreshToken);
        window.location.href = '/';
      } catch (error) {
        alert('로그인 실패. 아이디와 비밀번호를 확인하세요.');
      }
    };

    const navigateBack = () => {
      window.location.href = '/';
    };

    return { username, password, handleLogin, navigateBack };
  },
};
</script>

<style scoped>
/* 페이지 스타일 */
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #1e3c72, #2a5298); /* 블루 톤의 세련된 배경 */
  font-family: 'Roboto', sans-serif;
}

/* 컨테이너 스타일 */
.login-container {
  background: white;
  padding: 40px 50px;
  border-radius: 15px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

/* 제목 스타일 */
h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 20px;
  text-align: left;
}

/* 레이블 스타일 */
label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

/* 입력 필드 스타일 */
input {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus {
  border-color: #007aff;
  box-shadow: 0 0 8px rgba(0, 122, 255, 0.4);
}

/* 버튼 스타일 */
button {
  width: 100%;
  padding: 12px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 로그인 버튼 스타일 */
.login-button {
  background-color: #007aff;
  color: white;
  margin-top: 15px;
}

.login-button:hover {
  background-color: #0056b3;
}

.login-button:active {
  transform: translateY(2px);
}

/* 뒤로가기 버튼 스타일 */
.back-button {
  margin-top: 15px;
  background-color: #e0e0e0;
  color: #333;
  font-size: 0.9rem;
}

.back-button:hover {
  background-color: #c0c0c0;
}

.back-button:active {
  transform: translateY(2px);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .login-container {
    padding: 30px 20px;
  }

  h1 {
    font-size: 1.8rem;
  }

  button {
    font-size: 0.9rem;
    padding: 10px 15px;
  }
}
</style>
