import { createRouter, createWebHistory } from 'vue-router';
import CreateProblem from '../components/CreateProblem.vue'
import AuthForm from '../components/AuthForm.vue'
import UserProblems from '../components/UserProblems.vue'
import AdminProblems from '../components/AdminProblems.vue'
import Home from '../components/Home.vue'

const routes = [
  {path: '/', component: Home,},
  {path: '/auth_form', component: AuthForm,},
  {path: '/create_problem', component: CreateProblem,},
  {path: '/user_problems', component: UserProblems,},
  {path: '/admin_problems', component: AdminProblems,},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;