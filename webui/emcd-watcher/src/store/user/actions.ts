
import { TelegramAuthModel } from "@/models/TelegramAuthModel";
import { ActionTree } from "vuex";
import { UserActionsTypes } from "../interfaces";
import { IRootState } from "../root/state";
import { MutationTypes } from "./mutations";
import { UserState } from "./state";
import { apiCall, apiRoutes } from '@/utils/api';
import router from "@/router";
import { Lang } from "@/models/Lang";
import { FAQQuestionAnswerModel } from "@/models/FAQQuestionAnswerModel";

export enum ActionTypes {
    USER_LOGIN = "USER_LOGIN",
    UPDATE_TOKEN = "UPDATE_TOKEN",
    UPDATE_USER = "UPDATE_USER",
    UPDATE_LANGS = "UPDATE_LANGS",
    ADD_QUESTION = "ADD_QUESTION",
    UPDATE_QUESTIONS = "UPDATE_QUESTIONS",
    UPDATE_QUESTION = "UPDATE_QUESTION",
}

export const actions: ActionTree<UserState, IRootState> & UserActionsTypes = {
    [ActionTypes.UPDATE_TOKEN]({ commit }, token: string) {
        commit(MutationTypes.UPDATE_TOKEN, token);
    },
    [ActionTypes.USER_LOGIN](
        { commit }, payload: TelegramAuthModel
    ) {
        apiCall<{access_token: string}>({url: apiRoutes.user.login, method: 'POST', data: payload})
        .then((x) => {
            commit(MutationTypes.UPDATE_TOKEN, x.access_token)
            commit(MutationTypes.UPDATE_USER, payload)

            router.push('/admin')
        }).catch(() => {
            alert("Sorry you can't be admin")
        })
    },
    [ActionTypes.UPDATE_USER](
        { commit }
    ) {
        apiCall<{user: TelegramAuthModel}>({url: apiRoutes.user.me, method: 'GET'})
        .then((x) => {
            commit(MutationTypes.UPDATE_USER, x.user)
            router.push('/admin')
        }).catch(() => {
            alert("Sorry you can't be admin")
        })
    },
    [ActionTypes.UPDATE_LANGS](
        { commit }
    ) {
        apiCall<Lang[]>({url: apiRoutes.lang.list, method: 'GET'})
        .then((x) => {
            console.log(x)
            commit(MutationTypes.UPDATE_LANGS, x)
        }).catch(() => {
            alert("Sorry you can't be admin")
        })
    },
    [ActionTypes.UPDATE_QUESTIONS](
        { commit }, langId: number
    ) {
        apiCall<FAQQuestionAnswerModel[]>({url: `${apiRoutes.question.list}/${langId}`, method: 'GET'})
        .then((x) => {
            commit(MutationTypes.UPDATE_QUESTIONS, x)
        })
        .catch(() => {
            alert("Sorry you can't be admin")
        })
    },
    [ActionTypes.ADD_QUESTION](
        { commit }, payload: FAQQuestionAnswerModel
    ) {
        apiCall<FAQQuestionAnswerModel>({url: apiRoutes.question.add, method: 'POST', data: payload})
        .then((x) => {
            commit(MutationTypes.ADD_QUESTION, x)
        })
        .catch(() => {
            alert("Sorry you can't be admin")
        })
    },
    [ActionTypes.UPDATE_QUESTION](
        { commit, dispatch }, payload: FAQQuestionAnswerModel
    ) {
        apiCall<FAQQuestionAnswerModel>({url: apiRoutes.question.update, method: 'PATCH', data: payload})
        .then((x) => {
            dispatch(ActionTypes.UPDATE_QUESTIONS, payload.langId)
        })
        .catch(() => {
            alert("Sorry you can't be admin")
        })
    },
};

