import { Store as VuexStore, CommitOptions, DispatchOptions } from "vuex";
import { IUserGettersTypes, UserActionsTypes, UserMutationsTypes } from "../interfaces";
import { UserState } from "./state";
  
  export type UserStoreModuleTypes<S = UserState> = Omit<
    VuexStore<S>,
    "commit" | "getters" | "dispatch"
  > & {
    commit<
      K extends keyof UserMutationsTypes,
      P extends Parameters<UserMutationsTypes[K]>[1]
    >(
      key: K,
      payload?: P,
      options?: CommitOptions
    ): ReturnType<UserMutationsTypes[K]>;
  } & {
    getters: {
      [K in keyof IUserGettersTypes]: ReturnType<IUserGettersTypes[K]>;
    };
  } & {
    dispatch<K extends keyof UserActionsTypes>(
      key: K,
      payload?: Parameters<UserActionsTypes[K]>[1],
      options?: DispatchOptions
    ): ReturnType<UserActionsTypes[K]>;
  };