<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <section>
    <div class="background" v-if="!gamePlaying"></div>
    <div class="circle"></div>
    <header>
      <a href="#"><img class="logo" src="@/assets/img/coffe_quiz_logo.png"/></a>
      <ul>
        <li><RouterLink to="/" @click="closeMenu"><ion-icon name="home-outline"></ion-icon><p>Accueil</p></RouterLink></li>
        <li><RouterLink to="/scores" @click="closeMenu"><ion-icon name="receipt-outline"></ion-icon><p>Scores</p></RouterLink></li>
        <li><RouterLink to="/admin" @click="closeMenu"><ion-icon name="lock-closed-outline"></ion-icon><p>Administration</p></RouterLink></li>
        <li @click="logout" v-if="token"><RouterLink to="/" @click="closeMenu"><ion-icon name="log-out-outline"></ion-icon><p>Déconnexion</p></RouterLink></li>
        <li id="closemenu"><ion-icon name="close-outline"></ion-icon></li>
        <li id="openmenu"><ion-icon name="menu-outline"></ion-icon></li>
      </ul>
  </header>

  <RouterView :token="token" @login-success="updateToken" />
  </section>
</template>


<script>

window.addEventListener('resize', function() {
    var header = document.querySelector('header');
    var windowWidth = window.innerWidth;
    
    if (windowWidth < 1000) {
        header.classList.add('open');
    } else {
        header.classList.remove('open');
    }
});



/***** OPEN & CLOSE BUTTON *****/


document.addEventListener('DOMContentLoaded', function() {
    var openMenuButton = document.getElementById('openmenu');
    var closeMenuButton = document.getElementById('closemenu');
    var header = document.querySelector('header');

    openMenuButton.addEventListener('click', function() {
        header.classList.add('open');
    });
    closeMenuButton.addEventListener('click', function() {
        header.classList.remove('open');
    });
});

import participationStorageService from "@/Services/ParticipationStorageService";
export default {
  name: 'App',
  props: {
    question: {
      type: Object
    }
  },
  emits: ['answer-selected'],
  data() {
    return {
      gamePlaying: 0,
      token: participationStorageService.getToken()
  };
  },
  methods: {
    closeMenu() {
      var header = document.querySelector('header');
      header.classList.remove('open');
    },
    logout() {
      participationStorageService.resetToken();
      this.token = '';
      this.$router.push('/');
    },
    updateToken(token) {
      this.token = token;
    }
  }
};
</script>