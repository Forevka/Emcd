<template>
  <div class="home">
    <telegram-login-button
    mode="callback"
    telegram-login="MakeForMeBot"
    @callback="userLogged"/>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import TelegramLoginButton from '@/components/TelegramLoginButton.vue';
import { TelegramAuthModel } from '@/models/TelegramAuthModel';

@Options({
  components: {
    TelegramLoginButton
  },
})
export default class Home extends Vue {
  userLogged (user: TelegramAuthModel) {
    console.log(user)
  }
}
</script>
