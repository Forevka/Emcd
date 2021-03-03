import { MutationTree } from "vuex";
import { RootMutationsTypes } from "../interfaces";
import { MutationTypes } from "./mutation-types";
import { IRootState } from "./state";

export const mutations: MutationTree<IRootState> & RootMutationsTypes = {
  [MutationTypes.UPDATE_VERSION](state: IRootState, payload: string) {
    state.version = payload;
  }
};