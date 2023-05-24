<template>
    <div class="content">
      <div>
        <div>
          <h1>Questions</h1>

          <table v-if="questions" id="table">
            <thead>
            <tr>
              <th>Question</th>
            </tr>
            </thead>
            <tbody v-if="questions.length">
              <tr v-for="question in questions" :key="question.id">
                <td><RouterLink :to="'/admin/questions/' + question.id">{{ question.title }}</RouterLink></td>
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
  import QuizApiService from "@/Services/QuizApiService.js";
  import '@/assets/bundles/tables/datatables.min.js'
  import '@/assets/bundles/tables/datatables.min.css'
  
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
                  url: "src/assets/bundles/tables/french.json"
              },
              scrollY: 200,
              } );
        });

        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  