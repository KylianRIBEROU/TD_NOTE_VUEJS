<template>
    <div class="ajout-questionnaire">
        <h2 class="title">Ajouter un questionnaire</h2>

        <label for="labelQuestionnaire" class="label">Nom du questionnaire :</label>
        <input type="text" id="labelQuestionnaire" v-model="nomQuestionnaire" class="input">

        <div v-for="(question, index) in questions" :key="index" class="question">
            <span>{{ question.label }} : </span>
            <span v-for="(choice, cIndex) in question.choices" :key="cIndex">
                <input type="radio" :id="'choice' + cIndex" :value="cIndex" v-model="question.selectedChoice">
                <label :for="'choice' + cIndex">{{ choice }}</label>
            </span>
            <i class="fas fa-times delete-icon" @click="deleteQuestion(index)"></i>
        </div>

        <button class="add-question-btn" @click="toggleAddQuestion">Ajouter une question</button>

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

            <button class="create-question-btn" @click="addQuestion">ajouter la question</button>
        </div>

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
        questions: [],
        showAddQuestion: false 
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
        console.log(this.questions);
        console.log(this.questions[0].choices[0]);
        const questionnaireData = {
            name: this.nomQuestionnaire,
            questions: this.questions.map(question => {
            return {
                title: question.label,
                type: question.choices.length === 2 ? "questionsimple" : "questionmultiple",
                answer: question.choices[question.selectedChoice],

                first_answer: question.choices[0],
                second_answer: question.choices[1],
                third_answer: question.choices[2] || null,
                fourth_answer: question.choices[3] || null
            };
            })
        };

        console.log(questionnaireData);

        axios.post("http://localhost:5000/flaskapi/v1.0/questionnairequestions", questionnaireData)
            .then(response => {
            console.log(response.data);
            console.log("Questionnaire créé avec succès !");
            this.resetFields();
            this.resetChampsQuestionnaire();


            const newQuestionnaire = {
            id: response.data.id, 
            name: response.data.name,
            };

            this.$emit('new-questionnaire', newQuestionnaire); 
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
            }
            else if (this.questionType === 'fourChoices' && (!this.choice1.trim() || !this.choice2.trim() || !this.choice3.trim() || !this.choice4.trim())) {
                alert("Veuillez entrer tous les choix.");
                return;
            }
            if (!this.questionLabel.trim()) {
                alert("Veuillez entrer un libellé pour la question.");
                return;
            }
            let newQuestion = {
                label: this.questionLabel,
                choices: [this.choice1, this.choice2, this.choice3, this.choice4].filter(choice => choice.trim() !== ''),
                selectedChoice: null 
            };
            this.questions.push(newQuestion);
            this.resetFields();
            this.showAddQuestion = false;
        },
        deleteQuestion(index) {
            this.questions.splice(index, 1);
        },
        resetFields() {
            this.questionLabel = '';
            this.choice1 = '';
            this.choice2 = '';
            this.choice3 = '';
            this.choice4 = '';
        },

        resetChampsQuestionnaire(){
            this.nomQuestionnaire = '';
            this.questions = [];
        }
    }
};
</script>