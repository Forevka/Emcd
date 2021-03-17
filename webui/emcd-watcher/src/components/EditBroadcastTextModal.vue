<template>
    <div data-backdrop="static" data-keyboard="false" class="modal fade" id="broadcastEditModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Change text for #{{broadcast.broadcastId}} {{langById(broadcast.langId)?.name}}</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <form>
                <div class="form-group">
                    <label for="recipient-name" class="col-form-label">Text</label>
                    <input type="text" class="form-control" id="recipient-name" v-model="broadcast.text">
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
import { Lang } from '@/models/Lang';

@Options({
  components: {
  },
})
export default class EditBroadcastTextModal extends Vue {
    broadcast = {
        broadcastId: -1,
        langId: -1,
        text: "",
    };

    async save() {
        // @ts-ignore
        window.$('#broadcastEditModal').modal('hide')
    }

    langById(langId: number) {
        return this.langs.filter(x => x.id == langId)[0];
    }

    get langs(): Lang[] {
        return this.$store.getters.getLangs;
    }
    
    mounted() {
        emitter.on<{broadcastId: number; langId: number; text: string}>('broadcastEditModalOpen', event => {
            this.broadcast = event;
        })
    }
}
</script>
