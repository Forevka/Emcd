<template>
    <div data-backdrop="static" data-keyboard="false" class="modal fade" id="faqEditModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Edit question</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <form>
                <div class="form-group">
                    <label for="recipient-name" class="col-form-label">Question:</label>
                    <input type="text" class="form-control" id="recipient-name" v-model="question.questionTranslation">
                </div>
                <div class="form-group">
                    <label for="message-text" class="col-form-label">Answer:</label>
                    <textarea class="form-control" id="message-text" v-model="question.answerTranslation"></textarea>
                </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" @click="save">Save</button>
            </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { emitter } from '@/utils/bus';
import { FAQQuestionAnswerModel } from '@/models/FAQQuestionAnswerModel';

@Options({
  components: {
  },
})
export default class EditModal extends Vue {
    question: FAQQuestionAnswerModel = {
        questionId: -1,
        langId: -1,
        questionTranslation: "",
        answerTranslation: "",
    };

    save() {
        // @ts-ignore
        window.$('#faqEditModal').modal('hide')
        console.log(this.question)
    }

    mounted() {
        emitter.on<FAQQuestionAnswerModel>('faqEditModalOpen', event => {
            this.question = event;
        })
    }
}
</script>
