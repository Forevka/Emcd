import { ActionTree } from "vuex";
import { RootActionsTypes } from "../interfaces";
import { ActionTypes } from "./action-types";
import { MutationTypes } from "./mutation-types";
import { IRootState } from "./state";

export const actions: ActionTree<IRootState, IRootState> & RootActionsTypes = {
  [ActionTypes.UPDATE_VERSION]({ commit }, payload: string) {
    commit(MutationTypes.UPDATE_VERSION, payload);
  },
};