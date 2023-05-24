<template>
  <div class="background2" :style="{ backgroundImage: `url(${backgroundImage})`}"></div>
  <div class="content">
    <div class="questionnaire">
      <div v-if="question" class="question">
        <h2 v-if="question.title" class="questiontext">{{ question.title }}</h2>
        <h3 v-if="question.text" class="questiontext">{{ question.text }}</h3>
        <ul>
          <li v-for="answer in question.possibleAnswers" :key="answer.id">
            <span v-if="answer.isCorrect"><b style="color:green">✅ {{ answer.text }}</b></span>
            <span v-else>{{ answer.text }}</span>
          </li>
        </ul>
        
      <!-- Bouton Edit -->
      <RouterLink :to="`/admin/questions/${question.id}/edit`">
        <button class="c-button c-button--gooey"> Editer cette question ❓
          <div class="c-button__blobs">
            <div></div>
            <div></div>
            <div></div>
          </div>
        </button>
      </RouterLink>

      <!-- Bouton Remove -->
      <RouterLink :to="`/admin/questions/${question.id}/edit`">
        <button @click="removeQuestion" class="c-button c-button--gooey c-button--red"> Supprimer cette question ❌
          <div class="c-button__blobs">
            <div></div>
            <div></div>
            <div></div>
          </div>
        </button>
      </RouterLink>

      </div>
      <div v-else>
        Chargement des questions...
      </div>

    </div>

    <div class="imgBox">
      <img src="@/assets/img/undraw_questions.svg">
    </div>

  </div>

  
</template>

<style>
h3
{
  margin: 10px 0;
}
</style>
  
  <script>
  import QuizApiService from "@/Services/QuizApiService.js";
  
  export default {
    data() {
      return {
        questionId: null,
        question: null,
        backgroundImage: '' 
      };
    },
    created() {
      this.loadQuestion();
    },
    methods: {
        async loadQuestion() {
        try {
            const questionId = this.$route.params.questionId;
            const response = await QuizApiService.getQuestionById(questionId);
            this.question = response.data;
            this.backgroundImage = this.question.image;
        } catch (error) {
            console.error(error);
        }
      },
      removeQuestion() {
      const questionId = this.$route.params.questionId;
      // Appeler la méthode pour supprimer la question avec l'ID donné
      QuizApiService.removeQuestion(questionId)
        .then(() => {
          // Rediriger vers la liste des questions après avoir supprimé la question
          this.$router.push('/admin');
        })
        .catch((error) => {
          console.error(error);
        });
    },
    },
  };
  </script>
  