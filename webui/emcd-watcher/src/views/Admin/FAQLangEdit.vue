<template>
    <div>
        <div class="controls">
            <b>{{lang.name}}</b>
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#faqEditModal" @click="openModal(0)">
                Add new
                <i class="fa fa-plus"></i>
            </button>
        </div>
        <div class="question-answer card mb-4 py-3" :class='{
            "border-left-primary": q.statusId === 1,
            "border-left-dark": q.statusId === 2,
        }' v-for="q in questions" :key="q.questionId">
            <div class="card-body">
                <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#faqEditModal" @click="openModal(q.questionId)">
                    Edit 
                    <i class="fa fa-edit"></i>
                </button>
                <div class="question-text">
                    {{q.questionTranslation}}
                </div>
                <div class="answer-text">
                    {{q.answerTranslation || "not defined for this language"}}
                </div>
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown"
                            role="button" data-toggle="dropdown" aria-haspopup="true"
                            aria-expanded="false">
                            Actions
                        </a>
                        <div class="dropdown-menu dropdown-menu-right animated--fade-in"
                            aria-labelledby="navbarDropdown">
                            <a class="dropdown-item" href="#">{{q.statusId == 1 ? 'Disable' : 'Enable'}}</a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {FAQQuestionAnswerModel} from '@/models/FAQQuestionAnswerModel';
import { Lang } from '@/models/Lang';
import {emitter} from '@/utils/bus';

@Options({
  components: {
  }
})
export default class FAQLangEdit extends Vue {
    questions: FAQQuestionAnswerModel[] = [
        {
            questionId: 1,
            langId: 1,
            questionTranslation: "test",
            answerTranslation: "answer",
            statusId: 1,
        },
        {
            questionId: 2,
            langId: 1,
            questionTranslation: "test2111111111111111",
            answerTranslation: "answer2",
            statusId: 1,
        },
        {
            questionId: 2,
            langId: 1,
            questionTranslation: "test2111111111111111",
            answerTranslation: "answer2",
            statusId: 2,
        },
    ]

    openModal(questionId: number) {
        if (questionId === 0) {
            emitter.emit('faqEditModalOpen', {
                questionId: 0,
                langId: this.langId,
                questionTranslation: "",
                answerTranslation: "",
                statusId: 1,
            })
            return;
        }
        const qq = this.questions.find((x) => x.questionId == questionId)
        emitter.emit('faqEditModalOpen', qq)
    }
    
    get langId() {
        return Number(this.$route.params.langId)
    }

    get lang(){
        return this.$store.getters.getLangs.filter((x: Lang) => x.id == this.langId)[0]
    }
}
</script>

<style lang="scss" scoped>
.question-answer {
    display: flex;
    justify-content: space-between;
    margin: 4rem;
    margin-right: 0;

    .card-body {
        display: inline-flex;

    }

    div {
        margin-right: 2rem;
        margin-left: 2rem;
    }

    button {
        display: inline-flex;

        i {
            margin-left: 5px;
            margin-top: 2px;
        }
    }
}

.controls {
    button {
        float: right;
    }
}

.question-text {
    width: 100%;
}
.answer-text {
    width: 100%;
}
</style>