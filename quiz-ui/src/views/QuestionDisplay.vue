<template>
    <div v-if="question" class="question">
      <p v-if="question.title" class="questiontext questiontitle">{{ question.title }}</p>
      <p v-if="question.text" class="questiontext">{{ question.text }}</p>
      <ul class="listanswers">
        <li @click="$emit('answer-selected', index)" v-for="(answer, index) in question.possibleAnswers" :key="index">
          <a>{{ answer.text }}</a>
        </li>
      </ul>
    </div>
    <div v-else>
      Chargement des questions...
    </div>
</template>

<script>
export default {
  name: 'QuestionDisplay',
  props: {
    question: {
      type: Object
    }
  },
  emits: ['answer-selected'],
};
</script>