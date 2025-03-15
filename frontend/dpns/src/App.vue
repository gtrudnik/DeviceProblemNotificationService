<template>
  <router-view></router-view>
</template>

<script>
//import CreateProblem from './components/CreateProblem.vue'
//import AuthForm from './components/AuthForm.vue'
import router from './router/router';

export default {
  router,
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
