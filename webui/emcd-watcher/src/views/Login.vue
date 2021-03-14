<template>
  <div class="content vertical-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 contents">
          <div class="row justify-content-center">
            <div class="col-md-12">
              <div class="form-block">
                <div class="mb-4">
                  <h3>Admin panel <strong>EMCD</strong></h3>
                </div>
                <telegram-login-button
                  mode="callback"
                  :telegram-login="telegramLogin"
                  @callback="userLogged"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import TelegramLoginButton from "@/components/TelegramLoginButton.vue";
import { TelegramAuthModel } from "@/models/TelegramAuthModel";
import {ActionTypes as UserActions} from "@/store/user/actions"

@Options({
  components: {
    TelegramLoginButton
  }
})
export default class Login extends Vue {
  userLogged(user: TelegramAuthModel) {
    this.$store.dispatch(UserActions.USER_LOGIN, user)
  }

  get telegramLogin() {
    return process.env.VUE_APP_API_URL
  }
}
</script>

<style lang="scss" scoped>
.vertical-center {
  min-height: 100%;  /* Fallback for browsers do NOT support vh unit */
  min-height: 100vh; /* These two lines are counted as one :-)       */

  display: flex;
  align-items: center;
}
</style>