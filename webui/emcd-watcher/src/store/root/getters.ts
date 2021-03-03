import { GetterTree } from "vuex";
import { IRootGettersTypes } from "../interfaces";
import { IRootState } from "./state";

export const getters: GetterTree<IRootState, IRootState> & IRootGettersTypes = {
  getVersion: (state: IRootState): string => {
    return state.version;
  }
};