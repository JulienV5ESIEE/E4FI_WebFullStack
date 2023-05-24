<template>
  <div class="content">
    <div class="textBox">
      <h2>Testez-vous<br>sur le <span>CAFE</span></h2>
      <p>Êtes-vous un vrai connaisseur de café ou simplement un amateur occasionnel ? Mettez vos connaissances à l'épreuve avec notre quiz sur le café et découvrez si vous êtes un expert en la matière !</p>
      <div v-if="registeredScores.length" class="scores">
        <div v-for="(scoreEntry, index) in registeredScores.slice(0, 3)" :key="scoreEntry.date" class="score">
          <span class="inline" v-if="index === 0">🥇</span>
          <span class="inline" v-else-if="index === 1">🥈</span>
          <span class="inline" v-else-if="index === 2">🥉</span>
          <b v-if="scoreEntry.playerName == playerName && scoreEntry.score == score">{{ scoreEntry.playerName }} - {{ scoreEntry.score }} points</b><p v-else>{{ scoreEntry.playerName }} - {{ scoreEntry.score }} points</p>
        </div>
      </div>
      <div v-else>
        Chargement des résultats en cours...
      </div>
      <router-link to="/new-quiz" class="button">
      <button class="c-button c-button--gooey"> Let's go ☕
        <div class="c-button__blobs">
          <div></div>
          <div></div>
          <div></div>
        </div>
      </button>
    </router-link>
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="display: block; height: 0; width: 0;">
        <defs>
          <filter id="goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"></feGaussianBlur>
            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo"></feColorMatrix>
            <feBlend in="SourceGraphic" in2="goo"></feBlend>
          </filter>
        </defs>
    </svg>
    </div>

    <div class="imgBox">
      <img src="@/assets/img/coffee_seed.png">
    </div>

    <ul class="thumb">
      <li><a href="mailto:leo.mesbah@edu.esiee.fr"><img src="@/assets/img/leo.jpg"></a></li>
      <li><a href="mailto:julien.sarrau@edu.esiee.fr"><img src="@/assets/img/julien.jpg"></a></li>
    </ul>

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
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/Services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
      score: participationStorageService.getParticipationScore(),
      playerName: participationStorageService.getPlayerName(),
    };
  },
  async created() {
    try {
      const response = await quizApiService.getQuizInfo();
      this.registeredScores = response.data.scores;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>
