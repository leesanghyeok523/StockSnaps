<template>
  <section class="features-section">
    <div v-for="feature in features" :key="feature.id" class="feature-card">
      <h3>{{ feature.title }}</h3>
      <p>{{ feature.description }}</p>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    features: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.features-section {
  display: flex;
  justify-content: space-around;
  padding: 50px 20px;
  background-color: #f9f9f9;
}

.feature-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 30%;
}

.feature-card h3 {
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.feature-card p {
  color: #666666;
}
</style>
