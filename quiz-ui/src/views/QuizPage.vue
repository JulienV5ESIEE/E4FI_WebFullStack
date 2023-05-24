<template>
  <div class="content">
    <div class="new-quiz">
      <h4>Bienvenue sur notre <span>QUIZ</span> !</h4>
      <p>Pour commencer, veuillez saisir votre nom :</p>
      <form @submit.prevent="launchNewQuiz">
        <div class="group">
          <input required="" type="text" class="input" v-model="username" />
          <span class="highlight"></span>
          <span class="bar"></span>
          <label>Nom</label>
        </div>
        
        <button type="submit" class="c-button c-button--gooey"> Je suis prêt 💡
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
    </svg>

      </form>
    </div>

    <div class="imgBox">
        <img src="@/assets/img/undraw_searching.svg">
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/Services/ParticipationStorageService";
export default {
  name: 'NewQuizPage',
  data() {
    return {
      username: ''
    }
  },
  methods: {
    launchNewQuiz() {
      // Stockage du nom du joueur
      participationStorageService.savePlayerName(this.username);
      const playerName = participationStorageService.getPlayerName();
      // Affichage du nom d'utilisateur dans la console
      console.log("Launch new quiz with", playerName);
      this.$router.push('/questions');
    }

  }
}
</script>