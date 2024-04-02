<template>
  <div class="ajout-questionnaire">
    <h2 class="title">Ajouter un questionnaire</h2>

    <label for="labelQuestionnaire" class="label">Nom du questionnaire :</label>
    <input type="text" id="labelQuestionnaire" v-model="nomQuestionnaire" class="input">

    <!-- Affichage des questions déjà créées -->
    <div v-for="(question, index) in questions" :key="index" class="question">
      <span>{{ question.label }} : </span>
      <span v-for="(choice, cIndex) in question.choices" :key="cIndex">
        <input type="radio" :id="'choice' + cIndex" :value="cIndex" v-model="question.selectedChoice">
        <label :for="'choice' + cIndex">{{ choice }}</label>
      </span>
      <i class="fas fa-times delete-icon" @click="deleteQuestion(index)"></i>
    </div>

    <!-- Bouton "Ajouter une question" -->
    <button class="add-question-btn" @click="toggleAddQuestion">Ajouter une question</button>

    <!-- Div pour ajouter une nouvelle question -->
    <div v-if="showAddQuestion" class="add-question-container">
      <label for="questionType"></label>
      <div class="radio-options">
        <input type="radio" id="twoChoices" value="twoChoices" v-model="questionType" class="radio-input">
        <label for="twoChoices" class="radio-label">Questionnaire à 2 réponses</label>
        <input type="radio" id="fourChoices" value="fourChoices" v-model="questionType" class="radio-input">
        <label for="fourChoices" class="radio-label">Questionnaire à 4 réponses</label>
      </div>

      <label for="questionLabel" class="label">Libellé de la question :</label>
      <input type="text" id="questionLabel" v-model="questionLabel" class="input">

      <div v-if="questionType === 'twoChoices'" class="choices">
        <label for="choice1" class="label">Choix 1 :</label>
        <input type="text" id="choice1" v-model="choice1" class="input">
        <label for="choice2" class="label">Choix 2 :</label>
        <input type="text" id="choice2" v-model="choice2" class="input">
      </div>

      <div v-if="questionType === 'fourChoices'" class="choices">
        <label for="choice1" class="label">Choix 1 :</label>
        <input type="text" id="choice1" v-model="choice1" class="input">
        <label for="choice2" class="label">Choix 2 :</label>
        <input type="text" id="choice2" v-model="choice2" class="input">
        <label for="choice3" class="label">Choix 3 :</label>
        <input type="text" id="choice3" v-model="choice3" class="input">
        <label for="choice4" class="label">Choix 4 :</label>
        <input type="text" id="choice4" v-model="choice4" class="input">
      </div>

      <!-- Bouton "Créer" pour ajouter la question -->
      <button class="create-question-btn" @click="addQuestion">ajouter la question</button>
    </div>

    <!-- Bouton "Créer" -->
    <button class="create-btn" @click="createQuestionnaire">Créer le questionnaire</button>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      nomQuestionnaire: '',
      questionType: 'twoChoices',
      questionLabel: '',
      choice1: '',
      choice2: '',
      choice3: '',
      choice4: '',
      questions: [], // Liste des questions déjà créées
      showAddQuestion: false // Contrôle l'affichage de la div pour ajouter une nouvelle question
    };
  },
  
  methods: {
    createQuestionnaire() {
      if (!this.nomQuestionnaire.trim()) {
        alert("Veuillez entrer un nom pour le questionnaire.");
        return;
      }

      if (this.questions.length === 0) {
        alert("Veuillez ajouter au moins une question au questionnaire.");
        return;
      }

      const questionnaireData = {
        name: this.nomQuestionnaire,
        questions: this.questions.map(question => {
          return {
            title: question.label,
            type: question.choices.length === 2 ? "question_simple" : "question_multiple",
            // Supposons que la première réponse soit toujours la bonne réponse
            answer: 0,
            // Supposons également que les choix soient toujours dans l'ordre
            first_choice: question.choices[0],
            second_choice: question.choices[1],
            third_choice: question.choices[2] || null,
            fourth_choice: question.choices[3] || null
          };
        })
      };

      axios.post("http://localhost:5000/flaskapi/v1.0/questionnairequestions", questionnaireData)
        .then(response => {
          console.log(response.data);
          console.log("Questionnaire créé avec succès !");
          this.resetFields();
          // Redirection ou autres actions après la création réussie
        })
        .catch(error => {
          console.error(error);
        });
    },

    toggleAddQuestion() {
      this.showAddQuestion = !this.showAddQuestion; 
    },
    
    addQuestion() {
      if (this.questionType === 'twoChoices' && (!this.choice1.trim() || !this.choice2.trim())) {
        alert("Veuillez entrer tous les choix.");
        return;
      } else if (this.questionType === 'fourChoices' && (!this.choice1.trim() || !this.choice2.trim() || !this.choice3.trim() || !this.choice4.trim())) {
        alert("Veuillez entrer tous les choix.");
        return;
      }      if (!this.questionLabel.trim()) {
        alert("Veuillez entrer un libellé pour la question.");
        return;
      }
      // Construire la question en fonction du type choisi
      let newQuestion = {
        label: this.questionLabel,
        choices: [this.choice1, this.choice2, this.choice3, this.choice4].filter(choice => choice.trim() !== ''), // Filtrer les choix vides
        selectedChoice: null // Initialiser la réponse sélectionnée à null
      };
      this.questions.push(newQuestion);
      this.resetFields();
      this.showAddQuestion = false;
    },
    deleteQuestion(index) {
      this.questions.splice(index, 1); // Supprimer la question à l'index spécifié
    },
    resetFields() {
      // Réinitialiser les valeurs des champs
      this.questionLabel = '';
      this.choice1 = '';
      this.choice2 = '';
      this.choice3 = '';
      this.choice4 = '';
    }
  }
};
</script>

<style scoped>

.delete-icon {
  margin-left: 10px; /* Ajout de marge entre la question et l'icône de croix */
  cursor: pointer;
  color: red; /* Couleur de l'icône de croix */
}

  .ajout-questionnaire {
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
  }
  
  .title {
    margin-bottom: 15px;
  }
  
  .radio-options {
    margin-bottom: 15px;
  }
  
  .radio-label {
    margin-right: 10px; /* Ajout de marge entre les boutons radio et les libellés */
  }
  
  .radio-input {
    margin-right: 5px; /* Ajout de marge entre chaque bouton radio */
  }
  
  .choices label {
    display: block;
    margin-bottom: 5px;
  }
  
  .choices input {
    margin-bottom: 10px;
  }
  
  .create-btn, .add-question-btn {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;    
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 10px; /* Ajout de marge entre les boutons */
  }
  
  .create-btn:hover, .add-question-btn:hover {
    background-color: #0056b3;
  }
  
  .add-question-container {
    margin-top: 20px; /* Ajout de marge au-dessus de la div pour ajouter une nouvelle question */
  }

  .create-question-btn {
  padding: 10px 20px;
  background-color: #28a745; /* Couleur verte pour le bouton Créer la question */
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.create-question-btn:hover {
  background-color: #218838; /* Couleur de survol pour le bouton Créer la question */
}
  </style>
  