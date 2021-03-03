
import { TelegramAuthModel } from "@/models/TelegramAuthModel";
import { ActionTree } from "vuex";
import { UserActionsTypes } from "../interfaces";
import { IRootState } from "../root/state";
import { MutationTypes } from "./mutations";
import { UserState } from "./state";
import { apiCall, apiRoutes } from '@/utils/api';

export enum ActionTypes {
    USER_LOGIN = "USER_LOGIN",
    UPDATE_TOKEN = "UPDATE_TOKEN",
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
        })
    },
};

