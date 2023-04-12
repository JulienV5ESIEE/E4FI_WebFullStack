<template>
  <div>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
    <div v-if="gameOver">
      <h2>Fin du quiz !</h2>
      <p>Bravo {{ playerName }}, ton score est de {{ score }} / {{ totalNumberOfQuestions }}</p>
    </div>
  </div>
</template>

<script>
import QuestionDisplay from "./QuestionDisplay.vue";
import participationStorageService from "@/Services/ParticipationStorageService";

export default {
  components: {
    QuestionDisplay,
  },
  data() {
    return {
      questions: [
        {
          text: "Quelle est la capitale de la France ?",
          answers: [
            "Londres",
            "Madrid",
            "Paris"
          ],
          correctAnswerIndex: 2
        },
        {
          text: "Quel est le plus grand océan du monde ?",
          answers: [
            "L'océan Pacifique",
            "L'océan Atlantique",
            "L'océan Indien"
          ],
          correctAnswerIndex: 0
        },
        {
          text: "Quel est le plus haut sommet du monde ?",
          answers: [
            "L'Everest",
            "Le Mont Blanc",
            "Le Kilimandjaro"
          ],
          correctAnswerIndex: 0
        },
        {
          text: "Qui a écrit Les Misérables ?",
          answers: [
            "Victor Hugo",
            "Albert Camus",
            "Gustave Flaubert"
          ],
          correctAnswerIndex: 0
        },
        {
          text: "Quel est le plus grand désert du monde ?",
          answers: [
            "Le Sahara",
            "Le désert de Gobi",
            "Le désert d'Atacama"
          ],
          correctAnswerIndex: 0
        },
      ],
      currentQuestionPosition: 1,
      currentQuestion: null,
      totalNumberOfQuestions: 0,
      score: 0,
      playerName: participationStorageService.getPlayerName(),
      gameOver: false,
    };
  },
  async created() {
    this.currentQuestion = this.questions[0];
    await this.loadQuestions();
    this.totalNumberOfQuestions = this.questions.length;
    await this.loadQuestionByPosition(1);
  },
  methods: {
    async loadQuestionByPosition(position) {
      this.currentQuestionPosition = position;
      this.currentQuestion = this.questions[position - 1];
      return this.currentQuestion;
    },
    async answerClickedHandler(answerIndex) {
      if (this.currentQuestion.correctAnswerIndex === answerIndex) {
        this.score++;
      }
      if (this.currentQuestionPosition === this.totalNumberOfQuestions) {
        this.gameOver = true;
      } else {
        await this.loadQuestionByPosition(this.currentQuestionPosition + 1);
      }
    },
    async loadQuestions() {
      return Promise.resolve(this.questions);
    },
    endQuiz() {
      this.gameOver = true;
    },
  },
};
</script>
