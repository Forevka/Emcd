export const settings = {
    API_SERVER: process.env.VUE_APP_API_URL
};

export const questionStatusChangeMap: { [key: number]: number } = {
    1: 2,
    2: 1,
}