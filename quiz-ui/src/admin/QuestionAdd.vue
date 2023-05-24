<template>
  <div class="content">
    <div class="textBox">
      <h1>Ajouter une question</h1>
      <form @submit.prevent="addQuestion">
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
          <input type="number" v-model="question.position" required/>
        </label>
        <label>
          Image de la question:
          <input type="file" accept="image/*" @change="handleImageUpload">
        </label>
        <img class="prevuImg" v-if="question.imagePreview" :src="question.imagePreview" alt="Image de prévisualisation">
        <h3>Réponses possibles:</h3>
        <ul>
          <li v-for="answer in question.possibleAnswers" :key="answer.id">
            <label>
              <input type="text" v-model="answer.text" required>
              <input type="radio" :name="'correctAnswer-' + question.id" @click="selectCorrectAnswer(answer)">
              Bonne réponse
            </label>
          </li>
        </ul>

        <button type="submit" class="c-button c-button--gooey"> Ajouter ➕
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

export default {
  data() {
    return {
      question: {
        title: '',
        text: '',
        image: '',
        imagePreview: '',
        possibleAnswers: [
          { id: 1, text: '', isCorrect: false },
          { id: 2, text: '', isCorrect: false },
          { id: 3, text: '', isCorrect: false },
          { id: 4, text: '', isCorrect: false },
        ],
      },
    };
  },
  methods: {
  selectCorrectAnswer(selectedAnswer) {
    this.question.possibleAnswers.forEach(answer => {
      answer.isCorrect = answer === selectedAnswer;
    });
  },
  addQuestion() {
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

      QuizApiService.addQuestion(questionData)
        .then(() => {
          this.$router.push('/admin');
        })
        .catch((error) => {
          console.error(error);
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
