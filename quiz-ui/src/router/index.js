import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuestionsManager from '../views/QuestionsManager.vue';
import QuizPage from '../views/QuizPage.vue';

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
      component: QuizPage
    },
    {
      path: '/questions',
      name: 'Questions',
      component: QuestionsManager
    }


    // SECURITY
  ]
})

export default router
