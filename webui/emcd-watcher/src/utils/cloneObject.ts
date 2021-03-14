export function cloneObject<O>(obj: O): O {
    return JSON.parse(JSON.stringify(obj))
}