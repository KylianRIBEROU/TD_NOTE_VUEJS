<template>
    <div>
        <div class="questionnaire-header">
            <h3 v-if="!isEditing">{{ questionnaire.name }}</h3>
            <input v-model="editedQuestionnaireName" v-if="isEditing" placeholder="Nouveau nom">
            <button v-if="!isEditing" @click="deleteQuestionnaire" class="delete-icon"><img src="../assets/trash.png" width="30" height="30">Supprimer</button>
            <button v-if="!isEditing" @click="editQuestionnaire">Modifier</button>
			<button v-if="isEditing" @click="editQuestionnaire">Annuler</button>
            <button v-if="isEditing" @click="saveEditQuestionnaire">Enregistrer</button>
        </div>
        <Question v-for="question in questions" :key="question.id" :question="question" @remove="deleteQuestion(question)" @update="updateQuestion(question)"></Question>
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
			questions: [],
			editedQuestionnaireName: '',
            isEditing: false
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
		editQuestionnaire() {
			this.editedQuestionnaireName = this.questionnaire.name;
			this.isEditing = !this.isEditing;
		},
		async saveEditQuestionnaire() {
			try {
				// Mise à jour distante dans le serveur
				await axios.put(`http://localhost:5000/flaskapi/v1.0/questionnaires/${this.questionnaire.id}`, { name: this.editedQuestionnaireName }); // put car on modifie la ressource entière
				// Mise à jour locale dans le parent
				this.$emit('update', {id : this.questionnaire.id})
				this.isEditing = false;
			} catch (error) {
				console.error('Error updating questionnaire name:', error);
			}
		},
		async updateQuestion(question){
			// maj locale de la question
			console.log(question);
			const response = await axios.get(`http://localhost:5000/flaskapi/v1.0/questions/${question.id}`);
			const questionUpdated = response.data;
			console.log(questionUpdated);
			const updatedQuestionIndex = this.questions.findIndex(questionActuelle => questionActuelle.id === question.id);
			if (updatedQuestionIndex !== -1) {
				this.questions[updatedQuestionIndex] = questionUpdated;
			}
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
        emits : ["remove", "update"]
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