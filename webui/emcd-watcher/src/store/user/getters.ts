import { GetterTree } from "vuex";
import { IUserGettersTypes } from "../interfaces";
import { IRootState } from "../root/state";
import { UserState } from "./state";

export const getters: GetterTree<UserState, IRootState> & IUserGettersTypes = {
  getToken: (state: UserState) => {
    return state.token;
  },
  getUser: (state: UserState) => {
    return state.user
  },  
  getLangs: (state: UserState) => {
    return state.langs
  },  
};