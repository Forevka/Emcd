import { Module, ModuleTree } from "vuex";
import { actions } from "./actions";
import { mutations } from "./mutations";
import { IRootState, state } from "./state";
import { getters } from './getters';
import userModule from "../user";

// Modules
const modules: ModuleTree<IRootState> = {
  userModule
};

const root: Module<IRootState, IRootState> = {
  state,
  getters,
  mutations,
  actions,
  modules
};

export default root;