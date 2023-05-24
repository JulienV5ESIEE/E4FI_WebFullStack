<template>
  <div class="content">
    <div>
      <h1>Vos <span>scores</span></h1>
      <div class="first" v-if="quizResults[0]">
      <span>🥇</span> <b v-if="quizResults[0].playerName == playerName && quizResults[0].score == score">{{ quizResults[0].playerName }} - {{ quizResults[0].score }} pts</b><p v-else>{{ quizResults[0].playerName }} - {{ quizResults[0].score }} pts</p>
      </div>

      <div class="secondandthird" v-if="quizResults[1] || quizResults[2]">
        <div v-if="quizResults[1]"><span>🥈</span> <b v-if="quizResults[1].playerName == playerName && quizResults[1].score == score">{{ quizResults[1].playerName }} - {{ quizResults[1].score }} pts</b><p v-else>{{ quizResults[1].playerName }} - {{ quizResults[1].score }} pts</p></div>
        <div v-if="quizResults[2]"><span>🥉</span> <b v-if="quizResults[2].playerName == playerName && quizResults[2].score == score">{{ quizResults[2].playerName }} - {{ quizResults[2].score }} pts</b><p v-else>{{ quizResults[2].playerName }} - {{ quizResults[2].score }} pts</p></div>
      </div>


      <table v-if="quizResults.length" id="table">
            <thead>
            <tr>
              <th>Nom</th>
              <th>Score</th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="(result, index) in quizResults.slice(3)" :key="index">
                <td><b v-if="result.playerName == playerName && result.score == score">{{ result.playerName }}</b><span v-else>{{ result.playerName }}</span></td>
                <td><b v-if="result.playerName == playerName && result.score == score">{{ result.score }}</b><span v-else>{{ result.score }}</span></td>
              </tr>
            </tbody>
        </table>

      <div v-else>
        Chargement des résultats en cours...
      </div>
    </div>
  <div class="imgBox">
    <img src="@/assets/img/undraw_progress.svg">
  </div>
  </div>
</template>

<style>

.content div
{
  margin: auto;
}

.content h1
{
    color: var(--color-black);
    font-size: 4em;
    line-height: 1.4em;
    font-weight: 500;
}

.content h1 span
{
  color: var(--main-color);
  font-size: 1em;
  font-weight: 900;
  text-decoration: underline;
}

.first
{
  text-align: center;
}

.first span
{
  font-size: 50px;
  display: block;
}

.secondandthird
{
  margin: 20px 0 !important;
  display: inline-flex;
  flex-flow: row wrap;
  justify-content: space-evenly;
  gap: 30px;
  width: 100%;
}

.secondandthird div
{
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.secondandthird div span
{
  display: block;
  font-size: 30px;
}

</style>

<script>
import QuizApiService from "@/services/QuizApiService.js";
import '@/assets/bundles/tables/datatables.min.js'
import '@/assets/bundles/tables/datatables.min.css'
import participationStorageService from "@/Services/ParticipationStorageService";

export default {
  name: "QuizResults",
  data() {
    return {
      quizResults: [],
      score: participationStorageService.getParticipationScore(),
      playerName: participationStorageService.getPlayerName(),
    };
  },
  async mounted() {
    const response = await QuizApiService.getQuizInfo();
    this.quizResults = response.data.scores;
    console.log(this.score);
    console.log(this.playerName);
    $(document).ready(function () {
      $('#table').DataTable({
          language: {
              url: "src/assets/bundles/tables/french.json"
          },
          scrollY: 120,
          order: [[ 1, "desc" ]] } );
    });
  },
};

</script>