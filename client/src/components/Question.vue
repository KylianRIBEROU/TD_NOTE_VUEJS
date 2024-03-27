<template>
    <div>
        <h4>{{ question.title }}</h4>
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
                <input type="radio" v-model="selectedAnswers" :value="question.first_answer"> {{ question.first_answer }}
            </label>
            <label>
                <input type="radio" v-model="selectedAnswers" :value="question.second_answer"> {{ question.second_answer }}
            </label>
            <label>
                <input type="radio" v-model="selectedAnswers" :value="question.third_answer"> {{ question.third_answer }}
            </label>
            <label>
                <input type="radio" v-model="selectedAnswers" :value="question.four_answer"> {{ question.four_answer }}
            </label>
        </div>
        <button @click="repondre">Répondre</button>
    </div>
</template>
  
<script>
    export default {
        props: ['question'],
        data() {
        return {
            selectedAnswer: null, // questions simples
            selectedAnswers: [] // questions multiples
        };
        },
        methods: {
        repondre() {
            // logique de réponse ici
        }
        }
    };
</script>
  