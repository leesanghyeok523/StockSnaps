import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('accessToken'), // 초기화 시 로컬스토리지 확인
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/token/', {
          username,
          password,
        });

        const { access, refresh } = response.data;

        // 토큰 저장
        this.accessToken = access;
        this.refreshToken = refresh;

        // Axios 헤더에 토큰 설정
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        this.isAuthenticated = true;

        // 로컬 스토리지에 토큰 저장
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        console.log('로그인 성공:', response.data);
      } catch (error) {
        console.error('로그인 실패:', error.response || error);
        throw new Error('로그인 실패');
      }
    },
    logout() {
      // 상태 초기화
      this.isAuthenticated = false;
      this.accessToken = null;
      this.refreshToken = null;

      // Axios 헤더 초기화
      delete axios.defaults.headers.common['Authorization'];

      // 로컬 스토리지에서 토큰 삭제
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');

      console.log('로그아웃 성공');
    },
  },
});
