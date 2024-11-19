// src/axiosInstance.js
import axios from 'axios';
import { getCSRFToken } from './utils/csrf';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Django 서버 주소
  withCredentials: true, // 쿠키를 포함한 요청 활성화
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCSRFToken(), // CSRF Token 추가
  },
});

export default axiosInstance;
