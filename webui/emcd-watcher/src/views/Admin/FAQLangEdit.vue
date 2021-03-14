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
                            <a class="dropdown-item" @click='changeStatus(q.questionId)'>{{q.statusId == 1 ? 'Disable' : 'Enable'}}</a>
                            <a class="dropdown-item" @click='deleteQuestion(q.questionId)'>Delete</a>
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
import {ActionTypes as UserActions} from "@/store/user/actions"
import {MutationTypes as UserMutations} from "@/store/user/mutations"
import {cloneObject } from "@/utils/cloneObject";

@Options({
  components: {
  }
})
export default class FAQLangEdit extends Vue {
    unsubscribeQuestions!: () => void;
    questions: FAQQuestionAnswerModel[] = []

    changeStatus(questionId: number) {
        console.log('change status', questionId)
    }

    deleteQuestion(questionId: number) {
        console.log('delete question', questionId)
    }

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
        emitter.emit('faqEditModalOpen', cloneObject(qq))
    }
    
    created() {
        this.unsubscribeQuestions = this.$store.subscribe((mutation: {type: string; payload: FAQQuestionAnswerModel[]}) => {
            console.log(mutation)
            if (mutation.type == UserMutations.UPDATE_QUESTIONS) {
                this.questions = mutation.payload;
            }
        })

        this.$store.dispatch(UserActions.UPDATE_QUESTIONS, this.langId)
    }

    unmounted() {
        this.unsubscribeQuestions()
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