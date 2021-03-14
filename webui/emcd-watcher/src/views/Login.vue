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
import {notification} from '@/utils/notification';

@Options({
  components: {
    TelegramLoginButton
  }
})
export default class Login extends Vue {
  async userLogged(user: TelegramAuthModel) {
    await this.$store.dispatch(UserActions.USER_LOGIN, user).then(() => {
      notification.success({
          title: 'Ok',
          message: 'Successfully logged'
      })
    }).catch(() => {
      notification.error({
          title: ':(',
          message: 'You dont have permissions'
      })
    })
  }

  get telegramLogin() {
    return process.env.VUE_APP_BOT_USERNAME
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