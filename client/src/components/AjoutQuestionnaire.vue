<template>
  <div class="ajout-questionnaire">
    <h2 class="title">Ajouter un questionnaire</h2>

    <label for="labelQuestionnaire" class="label">Nom du questionnaire :</label>
    <input type="text" id="labelQuestionnaire" v-model="nomQuestionnaire" class="input">

    <!-- Affichage des questions déjà créées -->
    <div v-for="(question, index) in questions" :key="index" class="question">
      <span>{{ question }}</span>
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
      <button class="create-question-btn" @click="addQuestion">Créer</button>
    </div>

    <!-- Bouton "Créer" -->
    <button class="create-btn" @click="createQuestionnaire">Créer</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      nomQuestionnaire: '',
      questionType: 'twoChoices',
      choices: [
        { value: '' },
        { value: '' },
        { value: '' },
        { value: '' }
      ], // Initialisation de 4 choix pour les questionnaires à 4 réponses
      questions: [], // Liste des questions déjà créées
      showAddQuestion: false // Contrôle l'affichage de la div pour ajouter une nouvelle question
    };
  },
  
  methods: {
    createQuestionnaire() {
      // Envoyer une requête POST à l'API avec les données du questionnaire
      const questionnaireData = {
        name: this.nomQuestionnaire,
        questions: this.questions // Inclure toutes les questions dans les données du questionnaire
      };
      // Exemple d'envoi de la requête POST (adapté à votre configuration)
      // axios.post('/flaskapi/v1.0/questionnaires', questionnaireData)
      //   .then(response => {
      //     console.log(response.data);
      //     // Rediriger ou faire d'autres actions après la création réussie
      //   })
      //   .catch(error => {
      //     console.error(error);
      //   });
    },
    toggleAddQuestion() {
      this.showAddQuestion = !this.showAddQuestion; // Inverser l'état de l'affichage de la div pour ajouter une nouvelle question
    },
    addQuestion() {
      // Construire la question en fonction du type choisi
      let newQuestion = '';
      if (this.questionType === 'twoChoices') {
        newQuestion = `Question avec 2 choix : ${this.choice1} et ${this.choice2}`;
      } else if (this.questionType === 'fourChoices') {
        newQuestion = `Question avec 4 choix : ${this.choice1}, ${this.choice2}, ${this.choice3} et ${this.choice4}`;
      }
      // Ajouter la question à la liste des questions
      this.questions.push(newQuestion);
      // Réinitialiser les champs de choix
      this.resetChoices();
      // Cacher la div pour ajouter une nouvelle question
      this.showAddQuestion = false;
    },
    resetChoices() {
      // Réinitialiser les valeurs des choix
      this.choice1 = '';
      this.choice2 = '';
      this.choice3 = '';
      this.choice4 = '';
    }
  }
};
</script>
  
  <style scoped>
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
  