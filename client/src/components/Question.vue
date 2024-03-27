<template>
    <div>
      <h4>{{ question.title }}</h4>
      <p v-if="question.question_type === 'questionsimple'">{{ question.first_answer }}, {{ question.second_answer }}</p>
      <p v-else-if="question.question_type === 'questionmultiple'">{{ question.first_answer }}, {{ question.second_answer }}, {{ question.third_answer }}, {{ question.four_answer }}</p>
      <button @click="repondre">Répondre</button>
    </div>
  </template>
  
  <script>
  export default {
    props: ['question'],
    methods: {
      repondre() {
        this.$router.push(`/repondre/${this.question.id}`)
      }
    }
  }
  </script>