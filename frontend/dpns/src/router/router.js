import { createRouter, createWebHistory } from 'vue-router';
import CreateProblem from '../components/CreateProblem.vue'
import AuthForm from '../components/AuthForm.vue'

const routes = [
  {path: '/auth_form', component: AuthForm,},
  {path: '/create_problem', component: CreateProblem,},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;