<template>
    <nav v-if="showNav" class="navbar navbar-expand-lg navbar-light bg-primary mb-3">
        <a class="navbar-brand text-white" style="font-size: 1.5rem;"><i class="fas fa-cog"></i>DPNS</a>
        <div class="collapse navbar-collapse d-flex justify-content-between align-items-center" id="navbarNav">
            <ul class="navbar-nav mx-auto">
                <li class="nav-item">
                    <router-link to="/user_problems" class="nav-link text-white"
                    style="font-size: 1.2rem;">Ваши заявки</router-link>
                </li>
                <li class="nav-item" v-if="role === 'admin' || role === 'super_admin'">
                    <router-link to="/admin_problems" class="nav-link text-white"
                    style="font-size: 1.2rem;">Проблемы</router-link>
                </li>
                <li class="nav-item" v-if="role === 'admin' || role === 'super_admin'">
                    <router-link to="/admin_devices" class="nav-link text-white"
                    style="font-size: 1.2rem;">Устройства</router-link>
                </li>
                <li class="nav-item" v-if="role === 'admin' || role === 'super_admin'">
                    <router-link to="/create_device" class="nav-link text-white"
                    style="font-size: 1.2rem;">Создать устройство</router-link>
                </li>
                <li class="nav-item" v-if="role === 'super_admin'">
                    <router-link to="/users" class="nav-link text-white"
                    style="font-size: 1.2rem;">Пользаватели</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/connect_tg" class="nav-link text-white"
                    style="font-size: 1.2rem;">Привязать телеграмм</router-link>
                </li>
            </ul>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <router-link to="#" @click.prevent="logout" class="nav-link text-white" style="font-size: 1.2rem;">Выйти</router-link>
                </li>
            </ul>
        </div>
    </nav>

    <router-view></router-view>
</template>

<script>
//import CreateProblem from './components/CreateProblem.vue'
//import AuthForm from './components/AuthForm.vue'
import router from './router/router';

import axios from 'axios';
axios.defaults.withCredentials = true;
export default {
  router,
  data() {
    return {
      role: localStorage.getItem('role'),
    };
  },
  computed: {
    showNav() {
        console.log(this.$route.path);
        return ['/create_device', '/admin_devices', '/admin_problems',
        '/user_problems', '/create_problem', '/connect_tg', '/users'].includes(this.$route.path) || this.$route.path.startsWith('/device/')
    },
  },
  created() {
  },
  watch: {
    $route() {
      if (!localStorage.getItem('role') && this.$route.path !== '/auth_form' && this.$route.path !== '/') {
        this.$router.push('/auth_form')
      } else if (localStorage.getItem('role') === "user" && !['/', '/auth_form',
            '/create_problem', '/user_problems', '/connect_tg'].includes(this.$route.path)) {
        this.$router.push('/')
      }
    }
  },
  methods: {
    async logout(){
        localStorage.removeItem('role')
        this.$router.push('/auth_form')
        await axios.post(`${this.$urlServer}/auth/logout`,);
    }
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
