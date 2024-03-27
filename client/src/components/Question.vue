<template>
    <div>
        <div class="question-header">
            <h4>{{ question.title }}</h4>
            <button @click="deleteQuestion" class="delete-icon"><img src="../assets/trash.png" width="30" height="30"></button>
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
            <input type="radio" v-model="selectedAnswer" :value="question.four_answer"> {{ question.four_answer }}
            </label>
        </div>
        <button @click="repondre">Répondre</button>
        <div v-if="reponseAffichee" :class="{ 'alert alert-success': reponseAffichee === 'Bonne réponse', 'alert alert-danger': reponseAffichee !== 'Bonne réponse' }">
            {{ reponseAffichee }}
        </div>
    </div>
  </template>
  
<script>
    export default {
        props: ['question'],
        data() {
            return {
                selectedAnswer: null,
                reponseAffichee: '' // afficher la réponse
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
                this.$emit('remove', {id:this.question.id});
            }
        },
        emits : ["remove"]
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
        background-color: #fff;
    }
</style>