<template>
    <div :class="{
            'loading': isShowing
        }">
        <img src="@/assets/loaderBlueTransparent.svg" v-if="isShowing"/>
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { emitter } from '@/utils/bus';

@Options({
  components: {}
})
export default class Loader extends Vue {
    isShowing = false;

    mounted() {
        emitter.on('show-loader', event => {
            this.isShowing = true;
        })
        
        emitter.on('hide-loader', event => {
            this.isShowing = false;
        })
    }
}
</script>

<style lang="scss" scoped>
/* Absolute Center Spinner */
.loading {
  position: fixed;
  left: 0%;
  top: 0px;
  width: 100%;
  height: 100%;
  z-index: 9999;
  display: flex;
  flex-flow: column wrap;
  justify-content: center;
  background: rgba(240, 248, 255, 0.5);
}
</style>