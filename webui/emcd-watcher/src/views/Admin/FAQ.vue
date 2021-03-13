<template>
    <div>
      <div>
        Please choose language to edit
      </div>
      <div class="available-langs">
        <router-link v-for="lang in langs" :key="lang.id" type="button" class="btn btn-primary" :to="`/admin/faq/${lang.id}`">{{lang.name}}</router-link>
      </div>
    </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";


@Options({
  components: {
  }
})
export default class FAQ extends Vue {
    get langs(){
        return this.$store.getters.getLangs
    }
}
</script>

<style lang="scss" scoped>
.available-langs {
  display: inline-flex;

  a {
    margin: 1rem;
  }
}
</style>