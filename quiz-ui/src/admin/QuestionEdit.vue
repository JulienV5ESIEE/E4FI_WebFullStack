<template>
  <div class="content">
    <div class="textBox">
      <h1>Page d'édition de la question</h1>
      <form @submit.prevent="editQuestion">
        <label>
          Titre de la question:
          <input type="text" v-model="question.title" required>
        </label>
        <label>
          Texte de la question:
          <textarea v-model="question.text" required></textarea>
        </label>
        <label>
            Position de la question:
            <input v-model="question.position" required/>
          </label>
        <label>
          Image de la question:
          <input type="file" accept="image/*" @change="handleImageUpload">
        </label>
        <img class="prevuImg" v-if="question.imagePreview" :src="question.imagePreview" alt="Image de prévisualisation">
        <h3>Réponses possibles:</h3>
        <ul class="possibleAnswers">
          <li v-for="answer in question.possibleAnswers" :key="answer.id">
            <label>
              <input type="text" v-model="answer.text" required>
              <input v-if="correctAnswer != answer.text" type="radio" :name="correctAnswer" @click="selectCorrectAnswer(answer)">
              <input v-if="correctAnswer == answer.text" type="radio" :name="correctAnswer" @click="selectCorrectAnswer(answer)" checked>
              Bonne réponse
            </label>
          </li>
        </ul>

        <button type="submit" class="c-button c-button--gooey"> Enregistrer 💾
          <div class="c-button__blobs">
            <div></div>
            <div></div>
            <div></div>
          </div>
        </button>

      </form>
    </div>
    <div class="imgBox">
        <img src="@/assets/img/undraw_questions.svg">
      </div>
  </div>
</template>

<script>
import QuizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      questionId: null,
      question: {
        id: '',
        title: '',
        text: '',
        image: null,
        imagePreview: '',
        correctAnswer: '',
        possibleAnswers: [
          { id: 1, text: '', isCorrect: false },
          { id: 2, text: '', isCorrect: false },
          { id: 3, text: '', isCorrect: false },
          { id: 4, text: '', isCorrect: false },
        ],
      },
    };
  },
  created() {
    this.loadQuestion();
  },
  methods: {
    selectCorrectAnswer(selectedAnswer) {
      this.question.possibleAnswers.forEach(answer => {
        answer.isCorrect = answer === selectedAnswer;
      });
    },
    async loadQuestion() {
      try {
        const questionId = this.$route.params.questionId;
        const response = await QuizApiService.getQuestionById(questionId);
        this.question = response.data;
        
        // Parcourir les réponses possibles pour trouver la réponse correcte
        for (const answer of this.question.possibleAnswers) {
          if (answer.isCorrect) {
            this.correctAnswer = answer['text'];
            break; // Sortir de la boucle une fois que la réponse correcte est trouvée
          }
        }

      } catch (error) {
        console.error(error);
      }
    },
    editQuestion() {
      const questionData = {
        text: this.question.text,
        title: this.question.title,
        image: this.question.image,
        position: parseInt(this.question.position),
        possibleAnswers: this.question.possibleAnswers.map(answer => ({
          text: answer.text,
          isCorrect: answer.isCorrect
        }))
      };

      QuizApiService.editQuestion(this.question.id, questionData)
        .then(() => {
          this.$router.push('/admin');
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            // Redirect to the login page
            participationStorageService.resetToken();
          } else {
            console.error(error);
          }
        });
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.question.image = reader.result; // Stocke l'image en base64 dans la propriété question.image
          this.question.imagePreview = URL.createObjectURL(file);
        };
        reader.readAsDataURL(file);
      }
    },
  },
};
</script>
