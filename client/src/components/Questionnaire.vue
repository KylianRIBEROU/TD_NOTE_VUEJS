<template>
	<div>
	  <div class="questionnaire-header">
		<h3 v-if="!isEditing">{{ questionnaire.name }}</h3>
		<button v-if="!isEditing" @click="deleteQuestionnaire" class="delete-icon"><img src="../assets/trash.png" width="30" height="30"></button>
		<button v-if="!isEditing" @click="editQuestionnaire">Modifier</button>
		<button @click="toggleDetails" class="toggle-details-btn">
		  <img v-if="!showDetails" src="../assets/down-arrow.png" alt="Down Arrow">
		  <img v-else src="../assets/up-arrow.svg" alt="Up Arrow">
		</button>
		<form v-if="isEditing" @submit.prevent="saveEditQuestionnaire">
		  <input v-model="editedQuestionnaireName" placeholder="Nouveau nom" required>
		  <button type="button" @click="editQuestionnaire">Annuler</button>
		  <button type="submit">Enregistrer</button>
		</form>
	  </div>
	  <div v-if="showDetails" class="questionnaire-content">
		<!-- Contenu du questionnaire -->
		<Question v-for="question in questions" :key="question.id" :question="question" @remove="deleteQuestion(question)" @update="updateQuestion(question)" class="conteneur-question"></Question>
		<div>
		  <button v-if="!showAddQuestion" class="btn-add-question" @click="showAddQuestionForm">Ajouter une question</button>
		  <!-- Formulaire d'ajout d'une question -->
		  <form v-if="showAddQuestion" @submit.prevent="addQuestion">
			<!-- Titre de la question -->
			<label>Titre de la question</label>
			<input type="text" v-model="newTitleQuestion" placeholder="Titre de la question" required>
			<!-- Type de question (simple ou multiple) -->
			<select v-model="newTypeQuestion" required>
			  <option value="questionsimple">Question simple</option>
			  <option value="questionmultiple">Question multiple</option>
			</select>
			<!-- Réponses (2 ou 4 inputs en fonction du type de question) -->
			<div v-if="newTypeQuestion === 'questionsimple'" class="div-choix">
				<label>1er choix</label>
				<input type="text" v-model="newFirstAnswer" placeholder="Première réponse" required>
				<label>2ème choix</label>
				<input type="text" v-model="newSecondAnswer" placeholder="Deuxième réponse" required>
			</div>
			<div v-else-if="newTypeQuestion === 'questionmultiple'" class="div-choix">
				<label>1er choix</label>
				<input type="text" v-model="newFirstAnswer" placeholder="Première réponse" required>
				<label>2ème choix</label>
				<input type="text" v-model="newSecondAnswer" placeholder="Deuxième réponse" required>
				<label>3ème choix</label>
				<input type="text" v-model="newThirdAnswer" placeholder="Troisième réponse" required>
				<label>4ème choix</label>
				<input type="text" v-model="newFourthAnswer" placeholder="Quatrième réponse" required>
			</div>
			<!-- Bonne réponse -->
			<label>Bonne réponse</label>
			<input type="text" v-model="newCorrectAnswerQuestion" placeholder="Bonne réponse" required>
			<button style="background-color: red" class="btn-add-question" @click="showAddQuestionForm">Annuler</button>
			<button type="submit" class="btn-add-question">Ajouter</button>
			<!-- Affichage de l'erreur si la bonne réponse n'existe pas parmi les réponses -->
			<div v-if="erreurReponseManquante" class="alert alert-danger">
			  La bonne réponse n'existe pas parmi les réponses disponibles.
			</div>
		  </form>
		</div>
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
		erreurReponseManquante: false,
		showDetails: false // Contrôle l'affichage du contenu du questionnaire
	  };
	},
	mounted() {
	  // Charge les questions associées à ce questionnaire lors du montage du composant
	  this.loadQuestions();
	},
	methods: {
	  async loadQuestions() {
		try {
		  // Requête pour obtenir les questions du questionnaire
		  const response = await axios.get(`http://localhost:5000/flaskapi/v1.0/questionnaires/${this.questionnaire.id}/questions`);
		  this.questions = response.data.questions;
		} catch (error) {
		  console.error('Error loading questions:', error);
		}
	  },
	  deleteQuestionnaire() {
		this.$emit('remove', { id: this.questionnaire.id });
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
		  this.$emit('update', { id: this.questionnaire.id });
		  this.isEditing = false;
		} catch (error) {
		  console.error('Error updating questionnaire name:', error);
		}
	  },
	  async updateQuestion(question) {
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
	  deleteQuestion(question) {
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
		if (this.newCorrectAnswerQuestion != this.newFirstAnswer && this.newCorrectAnswerQuestion != this.newSecondAnswer && this.newCorrectAnswerQuestion != this.newThirdAnswer && this.newCorrectAnswerQuestion != this.newFourthAnswer) {
		  // afficher à l'utilisateur que la bonne réponse n'existe pas dans les réponses
		  console.log("Bonne réponse n'existe pas dans les réponses");
		  this.erreurReponseManquante = true;
		}
		else {
		  const newQuestionData = {
			title: this.newTitleQuestion,
			answer: this.newCorrectAnswerQuestion,
			question_type: this.newTypeQuestion,
			first_answer: this.newFirstAnswer,
			second_answer: this.newSecondAnswer,
			third_answer: this.newThirdAnswer,
			fourth_answer: this.newFourthAnswer,
			questionnaire_id: this.questionnaire.id
		  };
  
		  // Envoie une requête POST pour ajouter la nouvelle question au serveur
		  axios.post(`http://localhost:5000/flaskapi/v1.0/questionnaire/${this.questionnaire.id}/questions`, newQuestionData)
			.then(response => {
			  // Ajoute la nouvelle question à la liste locale de questions
			  const newQuestion = response.data;
			  this.questions.push(newQuestion);
			  console.log('Question ajoutée avec succès : ', newQuestion);
			})
			.catch(error => {
			  console.error('Erreur lors de l\'ajout de la question : ', error);
			});
  
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
	  toggleDetails() {
		this.showDetails = !this.showDetails; // Inverse la valeur de showDetails
	  },
	  emits: ["remove", "update"]
	}
  }
  </script>
  
  <style scoped>
  h3 {
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
  
  .toggle-details-btn {
	background-color: transparent;
	border: none;
	cursor: pointer;
  }
  
  .toggle-details-btn img {
	width: 30px;
	height: 30px;
  }
  </style>
  