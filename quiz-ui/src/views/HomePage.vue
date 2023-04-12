<template>
  <div>
    <h1>Home page</h1>

    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>

    <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
  </div>
</template>


<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    try {
      const response = await quizApiService.getQuizInfo();
      this.registeredScores = response.data.scores;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>
