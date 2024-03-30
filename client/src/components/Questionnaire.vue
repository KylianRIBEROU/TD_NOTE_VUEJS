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
        <div>
            <button v-if="!showAddQuestion" class="btn-add-question" @click="showAddQuestionForm">Ajouter une question</button>
            <!-- Formulaire d'ajout d'une question -->
            <form v-if="showAddQuestion" @submit.prevent="addQuestion">
                <!-- Titre de la question -->
                <input type="text" v-model="newTitleQuestion" placeholder="Titre de la question" required>
                <!-- Type de question (simple ou multiple) -->
                <select v-model="newTypeQuestion" required>
                    <option value="questionsimple">Question simple</option>
                    <option value="questionmultiple">Question multiple</option>
                </select>
                <!-- Réponses (2 ou 4 inputs en fonction du type de question) -->
                <div v-if="newTypeQuestion === 'questionsimple'">
                    <input type="text" v-model="newFirstAnswer" placeholder="Première réponse" required>
                    <input type="text" v-model="newSecondAnswer" placeholder="Deuxième réponse" required>
                </div>
                <div v-else-if="newTypeQuestion === 'questionmultiple'">
                    <input type="text" v-model="newFirstAnswer" placeholder="Première réponse" required>
                    <input type="text" v-model="newSecondAnswer" placeholder="Deuxième réponse" required>
                    <input type="text" v-model="newThirdAnswer" placeholder="Troisième réponse" required>
                    <input type="text" v-model="newFourthAnswer" placeholder="Quatrième réponse" required>
                </div>
                <!-- Bonne réponse -->
                <input type="text" v-model="newCorrectAnswerQuestion" placeholder="Bonne réponse" required>
                <button class="btn-add-question" @click="showAddQuestionForm">Annuler</button>
                <button type="submit" class="btn-add-question">Ajouter</button>
                <!-- Affichage de l'erreur si la bonne réponse n'existe pas parmi les réponses -->
                <div v-if="erreurReponseManquante" class="alert alert-danger">
                    La bonne réponse n'existe pas parmi les réponses disponibles.
                </div>
            </form>
        </div>
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
            isEditing: false,
			showAddQuestion: false,
			newTitleQuestion: '',
			newTypeQuestion: 'questionsimple',
			newFirstAnswer: '',
			newSecondAnswer: '',
			newThirdAnswer: '',
			newFourthAnswer: '',
			newCorrectAnswerQuestion: '',
			erreurReponseManquante: false
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
		showAddQuestionForm() {
			this.showAddQuestion = !this.showAddQuestion;
		},
		addQuestion() {
			// gérer que la nouvelle réponse n'existe pas dans les réponses
			if (this.newCorrectAnswerQuestion != this.newFirstAnswer && this.newCorrectAnswerQuestion != this.newSecondAnswer && this.newCorrectAnswerQuestion != this.newThirdAnswer && this.newCorrectAnswerQuestion != this.newFourthAnswer){
				// afficher à l'utilisateur que la bonne réponse n'existe pas dans les réponses
				console.log("Bonne réponse n'existe pas dans les réponses");
				this.erreurReponseManquante = true;
            }
			else{
				// Ajout de la nouvelle question sur le serveur
				console.log("Question ajoutée en distant et local")
				// Ajout de la nouvelle question en local

				// Réinitialise le formulaire
				this.resetAddQuestionForm();
			}
		},
		resetAddQuestionForm() {
			this.showAddQuestion = false;
			this.newTitleQuestion = '';
			this.newTypeQuestion = 'questionsimple';
			this.newFirstAnswer = '';
			this.newSecondAnswer = '';
			this.newThirdAnswer = '';
			this.newFourthAnswer = '';
			this.newCorrectAnswerQuestion = '';
			this.erreurReponseManquante = false;
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

	.btn-add-question{
		background-color: #001f3f;
	}
</style>