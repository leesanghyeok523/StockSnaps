<template>
  <div class="signup-page">
    <div class="signup-container">
      <h1>회원가입</h1>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="username">아이디</label>
          <input id="username" v-model="formData.username" type="text" placeholder="아이디를 입력하세요" required />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input id="password" v-model="formData.password" type="password" placeholder="비밀번호를 입력하세요" required />
        </div>
        <div class="form-group">
          <label for="email">이메일</label>
          <input id="email" v-model="formData.email" type="email" placeholder="이메일을 입력하세요" required />
        </div>
        <div class="form-group">
          <label for="dob">생년월일</label>
          <input id="dob" v-model="formData.date_of_birth" type="date" required />
        </div>
        <button type="submit" class="signup-button">회원가입</button>
      </form>
      <button class="back-button" @click="navigateBack">뒤로가기</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  setup() {
    const formData = ref({
      username: '',
      password: '',
      email: '',
      date_of_birth: '',
    });

    const handleSignup = async () => {
      try {
        await axios.post('http://127.0.0.1:8000/signup/', formData.value);
        alert('회원가입 성공!');
        window.location.href = '/login'; // 로그인 페이지로 이동
      } catch (error) {
        console.error('회원가입 실패:', error.response.data);
        alert('회원가입 실패. 다시 시도해주세요.');
      }
    };

    const navigateBack = () => {
      window.location.href = '/';
    };

    return { formData, handleSignup, navigateBack };
  },
};
</script>

<style scoped>
.signup-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  font-family: 'Roboto', sans-serif;
}

.signup-container {
  background: white;
  padding: 30px 40px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus {
  border-color: #ff4e50;
  box-shadow: 0 0 5px rgba(255, 78, 80, 0.5);
}

button {
  width: 100%;
  padding: 10px 15px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.signup-button {
  background-color: #ff4e50;
  color: white;
  margin-top: 10px;
}

.signup-button:hover {
  background-color: #e84343;
}

.back-button {
  margin-top: 15px;
  background-color: #e0e0e0;
  color: #333;
}

.back-button:hover {
  background-color: #c0c0c0;
}

.signup-container button:active {
  transform: translateY(1px);
}
</style>
