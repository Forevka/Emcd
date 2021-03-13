import { IRootState } from "./store/root/state";
import { Store } from "@/store";

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $store: Store<IRootState>;
  }
}