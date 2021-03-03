import { ActionContext } from "vuex";
import { MutationTypes as RootMTypes } from "./root/mutation-types";
import { ActionTypes as RootATypes } from "./root/action-types";
import { MutationTypes as UserMTypes } from "./user/mutations";
import { ActionTypes as UserATypes } from "./user/actions";
import { IRootState } from "./root/state";
import { UserState } from "./user/state";
import { TelegramAuthModel } from "@/models/TelegramAuthModel";

export interface IMergedState extends IRootState {
    // merged modules
    // counterModule: CounterStateTypes;
}

export interface IRootGettersTypes {
  getVersion(state: IRootState): string;
}

export type RootMutationsTypes<S = IRootState> = {
  [RootMTypes.UPDATE_VERSION](state: S, payload: string): void;
};

type AugmentedActionContextRoot = {
  commit<K extends keyof RootMutationsTypes>(
    key: K,
    payload: Parameters<RootMutationsTypes[K]>[1]
  ): ReturnType<RootMutationsTypes[K]>;
} & Omit<ActionContext<IRootState, IRootState>, "commit">;

export interface RootActionsTypes {
  [RootATypes.UPDATE_VERSION](
    { commit }: AugmentedActionContextRoot,
    payload: string
  ): void;
}



export interface IUserGettersTypes {
  getToken(state: UserState): string | null;
}

export type UserMutationsTypes<S = UserState> = {
  [UserMTypes.UPDATE_TOKEN](state: S, payload: string): void;
}


type AugmentedActionContextUser = {
  commit<K extends keyof UserMutationsTypes>(
    key: K,
    payload: Parameters<UserMutationsTypes[K]>[1]
  ): ReturnType<UserMutationsTypes[K]>;
} & Omit<ActionContext<UserState, IRootState>, "commit">;


export interface UserActionsTypes {
  [UserATypes.UPDATE_TOKEN](
    { commit }: AugmentedActionContextUser,
    payload: string
  ): void;
  [UserATypes.USER_LOGIN](
    { commit }: AugmentedActionContextUser,
    payload: TelegramAuthModel
  ): void;
}


export interface StoreActions
  extends RootActionsTypes, UserActionsTypes {}
export interface StoreGetters
  extends IRootGettersTypes, IUserGettersTypes {}