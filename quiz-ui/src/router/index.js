import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuestionsManager from '../views/QuestionsManager.vue';

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
      component: QuestionsManager
    },
  ]
})

export default router