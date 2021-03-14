export enum MutationTypes {
    UPDATE_TOKEN = "UPDATE_TOKEN",
    USER_LOGOUT = "USER_LOGOUT",
    UPDATE_USER = "UPDATE_USER",
    UPDATE_LANGS = "UPDATE_LANGS",
    ADD_QUESTION = "ADD_QUESTION",
    UPDATE_QUESTIONS = "UPDATE_QUESTIONS",
}

import { FAQQuestionAnswerModel } from "@/models/FAQQuestionAnswerModel";
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
  [MutationTypes.USER_LOGOUT](state: UserState,) {
    localStorage.removeItem('user-token')
  },
  [MutationTypes.UPDATE_USER](state: UserState, payload: TelegramAuthModel) {
    state.user = payload;
  },
  [MutationTypes.UPDATE_LANGS](state: UserState, payload: Lang[]) {
    state.langs = payload;
  },
  [MutationTypes.ADD_QUESTION](state: UserState, payload: FAQQuestionAnswerModel) {
    state.questions.push(payload);
  },
  [MutationTypes.UPDATE_QUESTIONS](state: UserState, payload: FAQQuestionAnswerModel[]) {
    state.questions = payload;
  },
};