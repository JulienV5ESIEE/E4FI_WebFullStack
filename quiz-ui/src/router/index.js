import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/new-quiz',
      name: 'Add quiz',
      component: () => import('../views/QuizPage.vue')
    },
    {
      path: '/questions',
      name: 'Questions',
      component: () => import('../views/Questions.vue')
    },
  ]
})

export default router
