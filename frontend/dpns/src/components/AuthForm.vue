<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h1 class="text-center">Авторизация</h1>
        <form @submit.prevent="handleLogin" class="mt-4">
          <div class="form-group">
            <label for="email">Email:</label>
            <input
              type="email"
              class="form-control"
              id="email"
              v-model="email"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Пароль:</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary btn-block">Войти</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
export default {
  name: 'auth_form',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async handleLogin() {
      const response = await axios.post('http://127.0.0.1:8000/auth/auth',
        {"user": this.email, "password": this.password},
      );
      this.email = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 100px;
}
</style>