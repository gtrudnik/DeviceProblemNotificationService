import { createRouter, createWebHistory } from 'vue-router';
import CreateProblem from '../components/CreateProblem.vue'
import CreateDevice from '../components/CreateDevice.vue'
import AuthForm from '../components/AuthForm.vue'
import UserProblems from '../components/UserProblems.vue'
import AdminProblems from '../components/AdminProblems.vue'
import AdminDevices from '../components/AdminDevices.vue'
import Device from '../components/Device.vue'
import ConnectTg from '../components/ConnectTg.vue'
import Home from '../components/Home.vue'
import Users from '../components/Users.vue'


const routes = [
  {path: '/', component: Home,},
  {path: '/auth_form', component: AuthForm,},
  {path: '/create_problem/:id', component: CreateProblem,},
  {path: '/device/:id', component: Device,},
  {path: '/create_device', component: CreateDevice,},
  {path: '/user_problems', component: UserProblems,},
  {path: '/admin_problems', component: AdminProblems,},
  {path: '/admin_devices', component: AdminDevices,},
  {path: '/connect_tg', component: ConnectTg,},
  {path: '/users', component: Users,},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;