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
export default {
  name: 'auth_form',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    handleLogin() {
      // Здесь вы можете добавить логику авторизации (например, API вызов)
      console.log('Email:', this.email);
      console.log('Пароль:', this.password);
      // Ресетить форму
      this.email = '';
      this.password = '';
      // Можно перенаправить пользователя после успешного входа
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 100px;
}
</style>