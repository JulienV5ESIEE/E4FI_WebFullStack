<template>
    <div class="content">
      <div>
        <div>
          <h1>Questions</h1>

          <table v-if="questions" id="table">
            <thead>
            <tr>
              <th>Question</th>
              <th>Position</th>
            </tr>
            </thead>
            <tbody v-if="questions.length">
              <tr v-for="question in questions" :key="question.id">
                <td><RouterLink :to="'/admin/questions/' + question.id">{{ question.text }}</RouterLink></td>
                <td>{{ question.position }}</td>
              </tr>
            </tbody>
            <div v-else>
              Chargement des questions en cours...
            </div>
          </table>
          
          <RouterLink :to="`/admin/questions/add`">
          <button class="c-button c-button--gooey"> Ajouter une question ❓
            <div class="c-button__blobs">
              <div></div>
              <div></div>
              <div></div>
            </div>
          </button>
          </RouterLink>
        </div>
      </div>
      <div class="imgBox">
        <img src="@/assets/img/undraw_questions.svg">
      </div>
    </div>
</template>
  
  <script>
  import QuizApiService from "@/services/QuizApiService.js";
  
  export default {
    data() {
      return {
        questions: [],
      };
    },
    created() {
      this.loadQuestions();
    },
    methods: {
      async loadQuestions() {
        try {
          const response = await QuizApiService.getQuestions();
          this.questions = response.data;

          
          $(document).ready(function () {
            $('#table').DataTable({
              language: {
                  url: "https://cdn.datatables.net/plug-ins/505bef35b56/i18n/French.json"
              },
              scrollY: 200,
              order: [[ 1, "asc" ]] } );
        });

        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  