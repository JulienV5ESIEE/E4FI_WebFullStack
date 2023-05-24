import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuestionsManager from '../views/QuestionsManager.vue';
import QuizPage from '../views/QuizPage.vue';
import ScoresManager from '../views/ScoresManager.vue';
import ConnectionLogin from "../security/ConnectionLogin.vue";
import QuestionAdd from "../admin/QuestionAdd.vue";
import QuestionList from "../admin/QuestionList.vue";
import QuestionView from "../admin/QuestionView.vue";
import QuestionEdit from "../admin/QuestionEdit.vue";
import ParticipationStorageService from '../services/ParticipationStorageService';

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
    },
    {
      path: '/scores',
      name: 'Scores',
      component: ScoresManager
    },
    {
      path: "/login",
      name: "Connexion",
      component: ConnectionLogin,
      props: {
        token: ''
      }
    },
    {
      path: "/admin",
      name: "QuestionList",
      component: QuestionList,
      meta: { requiresAuth: true }
    },
    {
      path: "/admin/questions/add",
      name: "QuestionAdd",
      component: QuestionAdd,
      meta: { requiresAuth: true }
    },
    {
      path: "/admin/questions/:questionId",
      name: "QuestionView",
      component: QuestionView,
      meta: { requiresAuth: true }
    },
    {
      path: "/admin/questions/:questionId/edit",
      name: "QuestionEdit",
      component: QuestionEdit,
      meta: { requiresAuth: true }
    },


    // SECURITY
  ]
})

export default router

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const accessToken = ParticipationStorageService.getToken();
    if (!accessToken) {
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
});

