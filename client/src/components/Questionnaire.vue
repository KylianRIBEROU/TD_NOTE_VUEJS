<template>
	<div>
		<h3>{{ questionnaire.name }}</h3>
		<Question v-for="question in questions" :key="question.id" :question="question"></Question>
	</div>
</template>

<script>
	import axios from 'axios';
	import Question from './Question.vue';

	export default {
	props: {
		questionnaire: Object
	},
	components: {
		Question
	},
	data() {
		return {
		questions: []
		};
	},
	mounted() {
		// charge les questions associées à ce questionnaire quand composant lancé
		this.loadQuestions();
	},
	methods: {
		async loadQuestions() {
		try {
			// requête pour obtenir les questions du questionnaire
			const response = await axios.get(`http://localhost:5000/flaskapi/v1.0/questionnaires/${this.questionnaire.id}/questions`);
			this.questions = response.data.questions;
		} catch (error) {
			console.error('Error loading questions:', error);
		}
		}
	}
	}
</script>  
<style scoped>
h3{
	text-decoration: underline;
}
</style>