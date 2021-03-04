import { TelegramAuthModel } from "@/models/TelegramAuthModel";

export interface UserState {
    token: string | null;
    user: TelegramAuthModel | null;
}

export const state: UserState = {
    token: null,
    user: null,
};