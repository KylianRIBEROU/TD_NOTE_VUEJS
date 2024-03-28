<template>
	<div>
		<div class="questionnaire-header">
            <h3>{{ questionnaire.name }}</h3>
            <button @click="deleteQuestionnaire" class="delete-icon"><img src="../assets/trash.png" width="30" height="30">Supprimer</button>
        </div>
		<Question v-for="question in questions" :key="question.id" :question="question" @remove="deleteQuestion(question)"></Question>
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
			}
			catch (error) {
				console.error('Error loading questions:', error);
			}
		},
		deleteQuestionnaire(){
			this.$emit('remove', {id: this.questionnaire.id})
		},
		updateQuestion(question){
			console.log(question);
			// Construire l'objet contenant les données à envoyer dans la requête PATCH
			// const requestData = {
			// 	title: question.editedTitle,
			// 	answer: question.editedAnswer
			// };

			// // Ajouter les réponses en fonction du type de question
			// if (question.question_type === 'questionsimple') {
			// 	requestData.first_answer = question.editedFirstAnswer;
			// 	requestData.second_answer = question.editedSecondAnswer;
			// } else if (question.question_type === 'questionmultiple') {
			// 	requestData.first_answer = question.editedFirstAnswer;
			// 	requestData.second_answer = question.editedSecondAnswer;
			// 	requestData.third_answer = question.editedThirdAnswer;
			// 	requestData.fourth_answer = question.editedFourthAnswer;
			// }

			// // Envoyer la requête PATCH avec les données mises à jour
			// axios.patch(`http://localhost:5000/flaskapi/v1.0/questions/${question.id}`, requestData)
			// 	.then(response => {
			// 		// Mise à jour locale des données de la question avec les données mises à jour
			// 		const updatedQuestionIndex = this.questions.findIndex(questionActuelle => questionActuelle.id === question.id);
			// 		if (updatedQuestionIndex !== -1) {
			// 			if (question.question_type === 'questionmultiple') {
			// 				this.questions[updatedQuestionIndex].third_answer = question.editedThirdAnswer;
			// 				this.questions[updatedQuestionIndex].fourth_answer = question.editedFourthAnswer;
			// 			}
			// 			this.questions[updatedQuestionIndex].title = question.editedTitle;
			// 			this.questions[updatedQuestionIndex].first_answer = question.editedFirstAnswer;
			// 			this.questions[updatedQuestionIndex].second_answer = question.editedSecondAnswer;
			// 			this.questions[updatedQuestionIndex].answer = question.editedAnswer;
			// 		}
			// 		console.log('Question updated: ', question.id);
			// 	})
			// 	.catch(error => {
			// 		console.error('Error updating question : ', error);
			// 	});
		},
		deleteQuestion(question){
			console.log(question);
			axios.delete(`http://localhost:5000/flaskapi/v1.0/questions/${question.id}`)
			.then(response => {
				this.questions = this.questions.filter(questionActuelle => questionActuelle.id !== question.id);
				console.log('Question deleted : ', question.id);
			})
			.catch(error => {
				console.error('Error deleting question : ', error);
			});
		},
        emits : ["remove"]
	}
	}
</script>  
<style scoped>
	h3{
		text-decoration: underline;
	}
	.questionnaire-header {
        display: flex;
        align-items: center;
    }

    .delete-icon {
        margin-left: 10px;
        cursor: pointer;
        background-color: #ff5000;
		color: #000000;
    }
</style>