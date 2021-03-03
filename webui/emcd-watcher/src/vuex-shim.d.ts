import { IRootState } from "./store/root/state";

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $store: Store<IRootState>;
  }
}