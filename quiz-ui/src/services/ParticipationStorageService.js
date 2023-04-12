export default {
  clear() {
    // Efface toutes les données stockées dans le local storage
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    // Stocke le nom du joueur dans le local storage sous la clé "playerName"
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    // Récupère le nom du joueur stocké dans le local storage sous la clé "playerName"
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    // Stocke le score de participation dans le local storage sous la clé "participationScore"
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    // Récupère le score de participation stocké dans le local storage sous la clé "participationScore"
    return window.localStorage.getItem("participationScore");
  }
};
