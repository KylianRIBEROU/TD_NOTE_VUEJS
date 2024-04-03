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
				}
				catch (error) {
					console.error('Error loading quizz : ', error);
				}
			},
			mapQuizz(quizz) {
				return quizz.map(questionnaire => ({
					id: questionnaire.id,
					name: questionnaire.name
				}));
			},
			deleteQuestionnaire(questionnaire){
			console.log(questionnaire);
				axios.delete(`http://localhost:5000/flaskapi/v1.0/questionnaires/${questionnaire.id}`)
				.then(response => {
					this.quizz = this.quizz.filter(questionnaireActuel => questionnaireActuel.id !== questionnaire.id);
					console.log('questionnaire deleted : ', questionnaire.id);
				})
				.catch(error => {
					console.error('Error deleting questionnaire : ', error);
				});
			},
			async updateQuestionnaire(questionnaire) {
				console.log(questionnaire);
				const response = await axios.get(`http://localhost:5000/flaskapi/v1.0/questionnaires/${questionnaire.id}`);
				const questionnaireUpdated = response.data;
				console.log(questionnaireUpdated);
				const updatedQuestionnaireIndex = this.quizz.findIndex(questionnaireActuel => questionnaireActuel.id === questionnaire.id);
				if (updatedQuestionnaireIndex !== -1) {
					this.quizz[updatedQuestionnaireIndex] = questionnaireUpdated;
				}
			},
			addNewQuestionnaire(newQuestionnaire) {
				this.quizz.push(newQuestionnaire);
			}
		}
	}
</script>

<template>
  <div class="container">
    <div class="left-pane">
      <h1>Les quizz</h1>
      <Questionnaire v-for="questionnaire of quizz" :questionnaire="questionnaire" :key="questionnaire.id" @remove="deleteQuestionnaire(questionnaire)" @update="updateQuestionnaire(questionnaire)" class="conteneur-questionnaire"></Questionnaire>
    </div>
    <div class="right-pane">
      <AjoutQuestionnaire @new-questionnaire="addNewQuestionnaire"></AjoutQuestionnaire>
    </div>
  </div>
</template>