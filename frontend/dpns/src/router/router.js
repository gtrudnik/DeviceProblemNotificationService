import { createRouter, createWebHistory } from 'vue-router';
import CreateProblem from '../components/CreateProblem.vue'
import AuthForm from '../components/AuthForm.vue'
import UserProblems from '../components/UserProblems.vue'

const routes = [
  {path: '/auth_form', component: AuthForm,},
  {path: '/create_problem', component: CreateProblem,},
  {path: '/user_problems', component: UserProblems,},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;