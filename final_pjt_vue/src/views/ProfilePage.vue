<template>
  <div class="profile-page">
    <h1>프로필 페이지</h1>
    <p>로그인한 사용자만 접근할 수 있습니다.</p>
  </div>
</template>

<script>
export default {
  name: 'ProfilePage',
};
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: Arial, sans-serif;
}
</style>
