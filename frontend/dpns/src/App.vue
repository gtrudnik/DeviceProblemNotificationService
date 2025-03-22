<template>
    <nav v-if="showNav" class="navbar navbar-expand-lg navbar-light bg-primary mb-3">
        <a class="navbar-brand text-white" href="#" style="font-size: 1.5rem;"><i class="fas fa-cog"></i> DPNS</a>
        <div class="collapse navbar-collapse d-flex justify-content-between align-items-center" id="navbarNav">
            <ul class="navbar-nav mx-auto"> <!-- Центрируем ссылки -->
                <li class="nav-item">
                    <router-link to="/admin_problems" class="nav-link text-white" style="font-size: 1.2rem;">Проблемы</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/admin_devices" class="nav-link text-white" style="font-size: 1.2rem;">Устройства</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/create_device" class="nav-link text-white" style="font-size: 1.2rem;">Создать устройство</router-link>
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

export default {
  router,
  computed: {
    showNav() {
        return ['/create_device', '/admin_devices', '/admin_problems'].includes(this.$route.path)
    },
  },
  created() {
    if (!localStorage.getItem('is_login')) {
      this.$router.push('/auth_form')
    }  // else if (localStorage.getItem('usernameW') && (this.isLogin)) {
      //this.$router.push('/home')
    // }
  },
  methods: {
    logout(){
        localStorage.removeItem('is_login')
        this.$router.push('/auth_form')
        console.log(1);
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
