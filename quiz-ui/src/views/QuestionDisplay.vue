<template>
  <div>
    <p>{{ question.text }}</p>
    <img v-if="question.image" :src="question.image" />
    <ul>
      <li v-for="(answer, index) in question.answers" :key="index">
        <a @click="$emit('answer-selected', index)">{{ answer }}</a>
      </li>
    </ul>
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
  emits: ['answer-selected']
};
</script>
