<template>
    <div>
        <div v-if="isEditing">
            <form @submit.prevent="updateQuestion">
                <label>Titre de la question</label>
                <input type="text" v-model="editedTitle" placeholder="Nouveau titre" class="input-large" required>
                <div v-if="question.question_type === 'questionsimple'" class="div-choix">
                    <label>1er choix</label>
                    <input type="text" v-model="editedFirstAnswer" placeholder="Première réponse" class="input-medium" required>
                    <label>2ème choix</label>
                    <input type="text" v-model="editedSecondAnswer" placeholder="Deuxième réponse" class="input-medium" required>
                </div>
                <div v-else-if="question.question_type === 'questionmultiple'" class="div-choix">
                    <label>1er choix</label>
                    <input type="text" v-model="editedFirstAnswer" placeholder="Première réponse" class="input-medium" required>
                    <label>2ème choix</label>
                    <input type="text" v-model="editedSecondAnswer" placeholder="Deuxième réponse" class="input-medium" required>
                    <label>3ème choix</label>
                    <input type="text" v-model="editedThirdAnswer" placeholder="Troisième réponse" class="input-medium" required>
                    <label>4ème choix</label>
                    <input type="text" v-model="editedFourthAnswer" placeholder="Quatrième réponse" class="input-medium" required>
                </div>
                <label>Bonne réponse</label>
                <input type="text" v-model="editedAnswer" placeholder="Bonne réponse" class="input-medium" required>
                <button style="background-color: red" @click="editQuestion">Annuler</button>
                <button type="submit">Enregistrer</button>
                <div v-if="erreurReponseManquante" class="alert alert-danger">
                    La bonne réponse n'existe pas parmi les réponses disponibles.
                </div>
            </form>
        </div>
        <div v-else>
            <div class="question-header">
                <h4>{{ question.title }}</h4>
                <button @click="deleteQuestion" class="delete-icon"><img src="../assets/trash.png" width="30" height="30"></button>
                <button @click="editQuestion" class="edit-icon">Modifier</button>
            </div>
            <div v-if="question.question_type === 'questionsimple'">
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.first_answer"> {{ question.first_answer }}
                </label>
                <label>
                    <input type="radio" v-model="selectedAnswer" :value="question.second_answer"> {{ question.second_answer }}
                </label>
            </div>
            <div v-else-if="question.question_type === 'questionmultiple'">
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
                    <input type="radio" v-model="selectedAnswer" :value="question.fourth_answer"> {{ question.fourth_answer }}
                </label>
            </div>
            <button @click="repondre">Répondre</button>
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
                reponseAffichee: '',
                isEditing: false,
                editedTitle: '',
                editedFirstAnswer: '',
                editedSecondAnswer: '',
                editedThirdAnswer: '',
                editedFourthAnswer: '',
                editedAnswer: '',
                erreurReponseManquante: false
            };
        },
        methods: {
            repondre() {
                if (this.selectedAnswer !== null) {
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
                this.editedTitle = this.question.title;
                this.editedFirstAnswer = this.question.first_answer;
                this.editedSecondAnswer = this.question.second_answer;
                this.editedThirdAnswer = this.question.third_answer;
                this.editedFourthAnswer = this.question.fourth_answer;
                this.editedAnswer = this.question.answer;
                this.isEditing = !this.isEditing;
                if (this.erreurReponseManquante){
                    this.erreurReponseManquante = false;
                }
            },
            updateQuestion() {
                if (this.editedAnswer != this.editedFirstAnswer && this.editedAnswer != this.editedSecondAnswer && this.editedAnswer != this.editedThirdAnswer && this.editedAnswer != this.editedFourthAnswer){
                    console.log("Bonne réponse n'existe pas dans les réponses");
                    this.erreurReponseManquante = true;
                }
                else{
                    // maj sur le serveur ici et non dans le parent car on n'arrive pas à l'envoyer au parent la questionUpdated
                    
                    const requestData = {
                        title: this.editedTitle,
                        answer: this.editedAnswer
                    };

                    requestData.first_answer = this.editedFirstAnswer;
                    requestData.second_answer = this.editedSecondAnswer;
                    if (this.question.question_type === 'questionmultiple') {
                        requestData.third_answer = this.editedThirdAnswer;
                        requestData.fourth_answer = this.editedFourthAnswer;   
                    }

                    axios.patch(`http://localhost:5000/flaskapi/v1.0/questions/${this.question.id}`, requestData)
                        .then(response => {
                            this.$emit('update', {id: this.question.id});
                            console.log('Question updated: ', this.question.id);
                        })
                        .catch(error => {
                            console.error('Error updating question : ', error);
                        });
                    this.isEditing = false;
                    this.erreurReponseManquante = false;
                }
            }
        },
        emits: ["remove", "update"]
    };
</script>
<style scoped>
    .delete-icon {
        margin-left: 10px;
        cursor: pointer;
        background-color: #fff;
    }
</style>