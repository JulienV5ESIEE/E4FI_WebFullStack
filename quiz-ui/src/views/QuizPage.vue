<template>
  <div class="new-quiz">
    <h1>Bienvenue sur notre quiz !</h1>
    <p>Pour commencer, veuillez saisir votre nom :</p>
    <form @submit.prevent="launchNewQuiz">
      <label>
        Nom :
        <input type="text" v-model="username" />
      </label>
      <button type="submit">Commencer le quiz</button>
    </form>
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
      // ...
      const playerName = participationStorageService.getPlayerName();
      // Affichage du nom d'utilisateur dans la console
      console.log("Launch new quiz with", playerName);
      this.$router.push('/questions');
    }

  }
}
</script>

<style>
.new-quiz {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

form {
  margin-top: 20px;
}
</style>
