export enum MutationTypes {
    UPDATE_TOKEN = "UPDATE_TOKEN",
    UPDATE_USER = "UPDATE_USER",
    UPDATE_LANGS = "UPDATE_LANGS"
}

import { Lang } from "@/models/Lang";
import { TelegramAuthModel } from "@/models/TelegramAuthModel";
import { MutationTree } from "vuex";
import { UserMutationsTypes } from "../interfaces";
import { UserState } from "./state";

export const mutations: MutationTree<UserState> & UserMutationsTypes = {
  [MutationTypes.UPDATE_TOKEN](state: UserState, payload: string) {
    state.token = payload;
    localStorage.setItem('user-token', state.token)
  },
  [MutationTypes.UPDATE_USER](state: UserState, payload: TelegramAuthModel) {
    state.user = payload;
  },
  [MutationTypes.UPDATE_LANGS](state: UserState, payload: Lang[]) {
    state.langs = payload;
  },
};