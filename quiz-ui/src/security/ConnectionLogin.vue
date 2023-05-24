<template>
    <div class="content">
      <div class="textBox">
        <h1>Administration</h1>
        <form @submit.prevent="login">
        <label>
            <div class="group">
              <input required="" type="password" class="input" v-model="password" />
              <span class="highlight"></span>
              <span class="bar"></span>
              <label>Mot de passe</label>
            </div>
        </label>
        <button type="submit" class="c-button c-button--gooey"> Connexion🚪
          <div class="c-button__blobs">
            <div></div>
            <div></div>
            <div></div>
          </div>
        </button>
        </form>
        <p v-if="loginError">Mauvais mot de passe</p>
    </div>
  </div>
  <div class="imgBox">
      <img src="@/assets/img/coffee_seed.png">
    </div>
</template>

<style>
.content .textBox span
{
  font-size: 30px;
}

.content .textBox .scores
{
  display: flex;
  margin: 10px 0;
  gap: 10px;
}

.content .textBox .scores .score
{
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>
  
<script>
  import QuizApiService from "@/Services/QuizApiService.js";
  import participationStorageService from "@/Services/ParticipationStorageService";
  export default {
    data() {
      return {
        password: '',
        loginError: false,
        token: ''
      };
    },
    methods: {
      login() {
        QuizApiService.login(this.password).then((data) => {
        // data is the returned value from the login function
        this.token = data.data.token;
        this.$emit('login-success', data.data.token); // Émettre l'événement avec le token
        participationStorageService.saveToken(this.token);
        // Rediriger vers la liste des questions une fois connecté
        this.$router.push('/admin');
      })
      .catch((error) => {
        console.error(error);
        this.loginError = true;
      });
        // Utiliser la valeur de this.password pour vérifier le mot de passe
        // Si le mot de passe est correct, obtenir la liste des questions via une autre requête au serveur
        // Si le mot de passe est incorrect, afficher un message d'erreur (this.loginError = true)
      },
    },
  };
</script>
  