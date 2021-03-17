export function formatDate(date: Date) {
    const value = new Date(date);
    return `${(value.getDate()).toString().padStart(2, "0")}/${(value.getMonth()+1).toString().padStart(2, "0")}/${value.getFullYear()}`;
}

export function formatTime(date: Date) {
    const value = new Date(date);
    return `${value.getHours().toString().padStart(2, "0")}:${value.getMinutes().toString().padStart(2, "0")}:${value.getSeconds().toString().padStart(2, "0")}`
}