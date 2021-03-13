import mitt from 'mitt';


export declare type EventType = string | symbol;
// eslint-disable-next-line
export declare type Handler<T = any> = (event: T) => void;
// eslint-disable-next-line
export declare type WildcardHandler = (type: EventType, event?: any) => void;
export declare type EventHandlerList = Array<Handler>;
export declare type WildCardEventHandlerList = Array<WildcardHandler>;
export declare type EventHandlerMap = Map<EventType, EventHandlerList | WildCardEventHandlerList>;

export const emitter: {
    all: EventHandlerMap;
    // eslint-disable-next-line
    on<T = any>(type: EventType, handler: Handler<T>): void;
    on(type: '*', handler: WildcardHandler): void;
    // eslint-disable-next-line
    off<T = any>(type: EventType, handler: Handler<T>): void;
    off(type: '*', handler: WildcardHandler): void;
    // eslint-disable-next-line
    emit<T = any>(type: EventType, event?: T): void;
    // eslint-disable-next-line
    emit(type: '*', event?: any): void;
} = mitt();