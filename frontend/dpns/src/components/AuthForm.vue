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
          <h6 v-if="bad_login" style="color: red;">*Неправильный логин или пароль</h6>
          <button type="submit" class="btn btn-primary btn-block">Войти</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
axios.defaults.withCredentials = true;
export default {
  name: 'auth_form',
  data() {
    return {
      email: '',
      password: '',
      previousRoute: null,
      bad_login: false,
    };
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.previousRoute = from.path;
    });
  },
  methods: {
    async handleLogin() {
      try {
          const response = await axios.post(`${this.$urlServer}/auth/auth`,
            {"user": this.email, "password": this.password},
          );
          console.log(response.data.access_token);
          this.email = '';
          this.password = '';
          localStorage.setItem('role', response.data.role)
          if (this.previousRoute !== "/"){
            this.$router.back();
          } else if (response.data.role === "admin"){
            this.$router.push('/admin_problems');
          } else {
            this.$router.push('/user_problems');
          }
          //this.$router.push(this.$store.state.previousRoute.fullPath);
      } catch (error) {
          if (error.response.status === 401) {
            this.bad_login = true;
            console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
          }
          console.error(error.response.data);
      }
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 100px;
}
</style>