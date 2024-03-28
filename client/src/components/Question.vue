<template>
    <div>
        <!-- Contenu pour la modification de la question -->
        <div v-if="isEditing">
            <!-- Ajoutez ici les champs pour la modification de la question -->
            <input type="text" v-model="editedTitle" placeholder="Nouveau titre">
            <!-- Affichage des réponses en fonction du type de question -->
            <div v-if="question.question_type === 'questionsimple'">
                <!-- Modification des réponses pour les questions simples -->
                <input type="text" v-model="editedFirstAnswer" placeholder="Première réponse">
                <input type="text" v-model="editedSecondAnswer" placeholder="Deuxième réponse">
            </div>
            <div v-else-if="question.question_type === 'questionmultiple'">
                <!-- Modification des réponses pour les questions multiples -->
                <input type="text" v-model="editedFirstAnswer" placeholder="Première réponse">
                <input type="text" v-model="editedSecondAnswer" placeholder="Deuxième réponse">
                <input type="text" v-model="editedThirdAnswer" placeholder="Troisième réponse">
                <input type="text" v-model="editedFourthAnswer" placeholder="Quatrième réponse">
            </div>
            <!-- Champ de modification pour la réponse -->
            <input type="text" v-model="editedAnswer" placeholder="Bonne réponse">
            <!-- Boutons pour annuler ou enregistrer les modifications -->
            <button @click="editQuestion">Annuler</button>
            <button @click="updateQuestion">Enregistrer</button>
        </div>
        <!-- Contenu de la question -->
        <div v-else>
            <div class="question-header">
                <h4>{{ question.title }}</h4>
                <button @click="deleteQuestion" class="delete-icon"><img src="../assets/trash.png" width="30" height="30"></button>
                <button @click="editQuestion" class="edit-icon">Modifier</button>
            </div>
            <!-- Affichage des réponses -->
            <div v-if="question.question_type === 'questionsimple'">
                <!-- Affichage des réponses pour les questions simples -->
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.first_answer"> {{ question.first_answer }}
                </label>
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.second_answer"> {{ question.second_answer }}
                </label>
            </div>
            <div v-else-if="question.question_type === 'questionmultiple'">
                <!-- Affichage des réponses pour les questions multiples -->
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.first_answer"> {{ question.first_answer }}
                </label>
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.second_answer"> {{ question.second_answer }}
                </label>
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.third_answer"> {{ question.third_answer }}
                </label>
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.four_answer"> {{ question.four_answer }}
                </label>
            </div>
            <!-- Bouton pour répondre à la question -->
            <button @click="repondre">Répondre</button>
            <!-- Affichage de la réponse -->
            <div v-if="reponseAffichee" :class="{ 'alert alert-success': reponseAffichee === 'Bonne réponse', 'alert alert-danger': reponseAffichee !== 'Bonne réponse' }">
                {{ reponseAffichee }}
            </div>
        </div>
    </div>
  </template>
  
<script>
    import axios from 'axios';

    export default {
        props: ['question'],
        data() {
            return {
                selectedAnswer: null,
                reponseAffichee: '', // Afficher la réponse
                isEditing: false, // Indique si la question est en cours de modification
                editedTitle: '', // Titre de la question en cours de modification
                editedFirstAnswer: '', // Première réponse en cours de modification
                editedSecondAnswer: '', // Deuxième réponse en cours de modification
                editedThirdAnswer: '', // Troisième réponse en cours de modification
                editedFourthAnswer: '', // Quatrième réponse en cours de modification
                editedAnswer: '' // Réponse en cours de modification
            };
        },
        methods: {
            repondre() {
                if (this.selectedAnswer !== null) {
                    // Vérifie si une réponse a été sélectionnée
                    if (this.selectedAnswer.toLowerCase() === this.question.answer.toLowerCase()) {
                        this.reponseAffichee = 'Bonne réponse';
                    }
                    else {
                        this.reponseAffichee = 'Mauvaise réponse';
                    }
                }
                else {
                    this.reponseAffichee = 'Veuillez sélectionner une réponse';
                }
            },
            deleteQuestion() {
                this.$emit('remove', { id: this.question.id });
            },
            editQuestion() {
                // Pré-rempli les champs avec les valeurs actuelles de la question
                this.editedTitle = this.question.title;
                this.editedFirstAnswer = this.question.first_answer;
                this.editedSecondAnswer = this.question.second_answer;
                this.editedThirdAnswer = this.question.third_answer;
                this.editedFourthAnswer = this.question.fourth_answer;
                this.editedAnswer = this.question.answer;
                this.isEditing = !this.isEditing; // Passe en mode édition ou non
            },
            updateQuestion() {


                // gérer que la nouvelle réponse n'existe pas dans les réponses
                
                
                //if (this.editedAnswer != this.editedFirstAnswer && this.editedAnswer != this.editedSecondAnswer && this.editedAnswer != this.editedThirdAnswer && this.editedAnswer != this.editedFourthAnswer)


                // maj en locale a faire









                // Mise à jour de la question sur le serveur ici et non dans le parent car on n'arrive pas ç l'envoyer au parent
                
                // Construction de l'objet contenant les données à envoyer dans la requête PATCH (maj non complete de la resource)
                const requestData = {
                    title: this.editedTitle,
                    answer: this.editedAnswer
                };

                // Ajouter les réponses en fonction du type de question
                requestData.first_answer = this.editedFirstAnswer;
                requestData.second_answer = this.editedSecondAnswer;
                if (this.question.question_type === 'questionmultiple') {
                    requestData.third_answer = this.editedThirdAnswer;
                    requestData.fourth_answer = this.editedFourthAnswer;   
                }

                // Envoyer la requête PATCH avec les données mises à jour
                axios.patch(`http://localhost:5000/flaskapi/v1.0/questions/${this.question.id}`, requestData)
                    .then(response => {
                        // Mise à jour locale des données de la question avec les données mises à jour




                        // const updatedQuestionIndex = this.questions.findIndex(questionActuelle => questionActuelle.id === question.id);
                        // if (updatedQuestionIndex !== -1) {
                        //     if (question.question_type === 'questionmultiple') {
                        //         this.questions[updatedQuestionIndex].third_answer = question.editedThirdAnswer;
                        //         this.questions[updatedQuestionIndex].fourth_answer = question.editedFourthAnswer;
                        //     }
                        //     this.questions[updatedQuestionIndex].title = question.editedTitle;
                        //     this.questions[updatedQuestionIndex].first_answer = question.editedFirstAnswer;
                        //     this.questions[updatedQuestionIndex].second_answer = question.editedSecondAnswer;
                        //     this.questions[updatedQuestionIndex].answer = question.editedAnswer;
                        // }




                        console.log('Question updated: ', this.question.id);
                    })
                    .catch(error => {
                        console.error('Error updating question : ', error);
                    });
                this.isEditing = false;
            }
        },
        emits: ["remove"]
    };
</script>
  
<style scoped>
    .question-header {
        display: flex;
        align-items: center;
    }
    
    .delete-icon {
        margin-left: 10px;
        cursor: pointer;
        background-color: #fff; /* Fond blanc pour l'icône de suppression */
    }
    
    .edit-icon {
        margin-left: 10px;
        cursor: pointer;
        background-color: #ff5000; /* Couleur de fond pour l'icône de modification */
        color: #ffffff; /* Couleur du texte pour l'icône de modification */
    }
</style>