<script>
import axios from 'axios';
import Questionnaire from './components/Questionnaire.vue';
import AjoutQuestionnaire from './components/AjoutQuestionnaire.vue';

let data = {
  quizz:[]
};

export default {
  data(){
    return data;
  },
  mounted() {
    this.loadQuizz();
  },
  components: { Questionnaire, AjoutQuestionnaire },
  methods: {
    async loadQuizz() {
        try {
            const response = await axios.get('http://localhost:5000/flaskapi/v1.0/questionnaires');
            this.quizz = this.mapQuizz(response.data.questionnaires);
        } catch (error) {
            console.error('Error loading quizz : ', error);
        }
    },
    mapQuizz(quizz) {
        return quizz.map(questionnaire => ({
            id: questionnaire.id,
            name: questionnaire.name
        }));
    }
  }
}
</script>

<template>
  <div class="container">
    <!-- Partie gauche avec les questionnaires -->
    <div class="left-pane">
      <h1>Les quizz</h1>
      <Questionnaire v-for="questionnaire of quizz" :questionnaire="questionnaire" :key="questionnaire.id"></Questionnaire>
    </div>
    
    <!-- Partie droite pour l'ajout d'un questionnaire et d'une question -->
    <div class="right-pane">
      <AjoutQuestionnaire></AjoutQuestionnaire>
    </div>
  </div>
</template>
<style scoped>
.container {
  display: flex;
}

.left-pane {
  flex: 1;
}

.right-pane {
  flex: 1;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
h1{
  margin-bottom: 50px;
}
</style>
