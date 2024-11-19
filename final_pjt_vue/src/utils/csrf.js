// src/utils/csrf.js
export function getCSRFToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('csrftoken=')) {
        cookieValue = cookie.substring('csrftoken='.length, cookie.length);
        break;
      }
    }
  }
  return cookieValue;
}
