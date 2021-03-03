import { Module } from "vuex";
import { getters } from "./getters";
import { actions } from "./actions";
import { mutations } from "./mutations";
import { UserState, state } from "./state";
import { IRootState } from "../root/state";

// Module
const userModule: Module<UserState, IRootState> = {
  state,
  getters,
  mutations,
  actions
};

export default userModule;