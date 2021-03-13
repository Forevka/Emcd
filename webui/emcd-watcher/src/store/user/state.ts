import { Lang } from "@/models/Lang";
import { TelegramAuthModel } from "@/models/TelegramAuthModel";

export interface UserState {
    token: string | null;
    user: TelegramAuthModel | null;
    langs: Lang[];
}

export const state: UserState = {
    token: null,
    user: null,
    langs: [],
};