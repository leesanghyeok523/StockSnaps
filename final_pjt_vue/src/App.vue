<template>
  <div id="app">
    <HeaderNav />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import HeaderNav from './components/HeaderNav.vue';
import Footer from './components/Footer.vue';

export default {
  components: {
    HeaderNav,
    Footer,
  },
  mounted() {
    document.title = '금융의 모든 것 | 쉽게 간편하게';
  },
};
</script>

<style>
@import './assets/global.css';
</style>
