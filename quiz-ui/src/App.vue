<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <!--<img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />-->
      <div class="navbar">
        <RouterLink to="/"><div class="logo">Quiz</div></RouterLink>
        <nav>
        <RouterLink to="/"><ion-icon name="home-outline"></ion-icon><p>Accueil</p></RouterLink>
        <RouterLink to="/"><ion-icon name="receipt-outline"></ion-icon><p>Scores</p></RouterLink>
        <RouterLink to="/"><ion-icon name="lock-closed-outline"></ion-icon><p>Administration</p></RouterLink>
      </nav>
      </div>
  </header>

  <div class="content">
    <RouterView />
  </div>
</template>

<style scoped>
</style>
