<template>
    <div>
        <div class="controls" v-if="isLoaded">
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
import { questionStatusChangeMap } from '@/settings';
import { showLoader, hideLoader } from '@/utils/loader';

@Options({
  components: {
  }
})
export default class FAQLangEdit extends Vue {
    isLoaded = false;
    unsubscribeQuestions!: () => void;
    questions: FAQQuestionAnswerModel[] = []

    changeStatus(questionId: number) {
        const qq = this.questions.find((x) => x.questionId == questionId)
        if (qq) {
            qq.statusId = questionStatusChangeMap[qq.statusId]
            this.$store.dispatch(UserActions.UPDATE_QUESTION, qq)
        }
    }

    deleteQuestion(questionId: number) {
        const qq = this.questions.find((x) => x.questionId == questionId)
        this.$store.dispatch(UserActions.DELETE_QUESTION, qq)
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
    
    async created() {
        this.unsubscribeQuestions = this.$store.subscribe((mutation: {type: string; payload: FAQQuestionAnswerModel[]}) => {
            if (mutation.type == UserMutations.UPDATE_QUESTIONS) {
                this.questions = mutation.payload;
            }
        })
        
        this.isLoaded = false;
        showLoader()
        await this.$store.dispatch(UserActions.UPDATE_QUESTIONS, this.langId).then(async () => {
            console.log(this.lang)
            if (this.lang === undefined) {
                console.log('lang not ok')
                await this.$store.dispatch(UserActions.UPDATE_LANGS).then(() => {
                    hideLoader()
                    this.isLoaded = true;
                })
            } else {
                console.log('lang ok')
                hideLoader()
                this.isLoaded = true;
            }
        })

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

.dropdown-item {
    cursor: pointer;
}

.question-text {
    width: 100%;
}
.answer-text {
    width: 100%;
}
</style>