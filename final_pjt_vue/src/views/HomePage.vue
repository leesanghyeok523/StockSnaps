<template>
  <div class="home-page">
    <HeroSection />
  </div>
</template>

<script>
import HeroSection from '../components/HeroSection.vue';

export default {
  components: {
    HeroSection,
  },
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
