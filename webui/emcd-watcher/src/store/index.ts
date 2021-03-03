import { createStore } from 'vuex'
import root from './root';
import { IRootState } from './root/state';
import { RootStoreModuleTypes } from './root/types';
import { UserStoreModuleTypes } from './user/types';

export const store = createStore<IRootState>(root);

type StoreModules = {
  user: UserStoreModuleTypes;
  root: RootStoreModuleTypes;
};

export type Store = UserStoreModuleTypes<Pick<StoreModules, "user">> &
  RootStoreModuleTypes<Pick<StoreModules, "root">>;