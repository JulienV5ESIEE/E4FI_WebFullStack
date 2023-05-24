<template>
  <div class="background2" :style="{ backgroundImage: `url(${backgroundImage})`}" v-if="gamePlaying"></div>
  <div class="content">
    <div class="questionnaire">
      <div v-if="totalNumberOfQuestions">
      <h2 v-if="gamePlaying">Question <b>{{ currentQuestionPosition }}</b> / {{ totalNumberOfQuestions }}</h2>
      <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" v-if="gamePlaying" />
      </div>
      <div v-else>
        Chargement du questionnaire...
      </div>
      <div v-if="gameOver">
        <h1>Quiz terminé !</h1>
        <p v-if="score">Bravo <b>{{ playerName }}</b>, ton score est de {{ score }} / {{ totalNumberOfQuestions }} !</p>
        <p v-else>Chargement...</p>
        <p>Ton classement</p>

        <RouterLink to="/scores">
        <button type="submit" class="c-button c-button--gooey"> Voir les scores 💯
        <div class="c-button__blobs">
          <div></div>
          <div></div>
          <div></div>
        </div>
      </button>
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="display: block; height: 0; width: 0;">
        <defs>
          <filter id="goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"></feGaussianBlur>
            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo"></feColorMatrix>
            <feBlend in="SourceGraphic" in2="goo"></feBlend>
          </filter>
        </defs>
      </svg></RouterLink>

      </div>
    </div>
    <div class="imgBox">
      <img src="@/assets/img/undraw_questions.svg">
    </div>
  </div>
</template>

<style>

h2
{
    color: var(--color-black);
    font-size: 2em;
    line-height: 1.4em;
    font-weight: 500;
    margin-bottom: 20px;
}

h1
{ 
    color: var(--color-black);
    font-size: 4em;
    line-height: 1.4em;
    font-weight: 500;
    margin-bottom: 20px;
}


</style>

<script>
import QuestionDisplay from "./QuestionDisplay.vue";
import participationStorageService from "@/Services/ParticipationStorageService";
import QuizApiService from "@/Services/QuizApiService.js";

export default {
  components: {
    QuestionDisplay,
  },
  data() {
    return {
    questions: [],
    currentQuestionPosition: 1,
    currentQuestion: null,
    totalNumberOfQuestions: 0,
    score: 0,
    playerName: participationStorageService.getPlayerName(),
    gameOver: false,
    gamePlaying: true,
    answers: [],
    backgroundImage: '' // Initialiser la valeur à une chaîne vide
  };
  },
  
  async created() {
    try {
      const response = await QuizApiService.getQuestions();
      this.questions = response.data;
      this.totalNumberOfQuestions = this.questions.length;
      await this.loadQuestionByPosition(1);
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async loadQuestionByPosition(position) {
      this.currentQuestionPosition = position;
      this.currentQuestion = this.questions[position - 1];
      this.backgroundImage = this.currentQuestion.image;
      return this.currentQuestion;
    },
    async answerClickedHandler(answerIndex) {
      this.answers.push(answerIndex+1);
      if (this.currentQuestionPosition === this.totalNumberOfQuestions) {
        this.gameOver = true;
        this.gamePlaying = false;
        // Appel de la méthode pour enregistrer les réponses
        QuizApiService.saveScore(this.playerName, this.answers).then((data)=>{
            // data is the returned value from the getFromDatabase function
            this.score = data.data.score;
            participationStorageService.saveParticipationScore(this.score);
        })

        //this.score = response.score; // Mettre à jour la variable this.score avec le score retourné
      } else {
        await this.loadQuestionByPosition(this.currentQuestionPosition + 1);
      }
    },
    async loadQuestions() {
      return Promise.resolve(this.questions);
    },
    endQuiz() {
      this.gameOver = true;
      this.gamePlaying = false;
    },
  },
};
</script>
