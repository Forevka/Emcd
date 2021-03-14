import axios, { AxiosRequestConfig } from "axios";
import { settings } from "@/settings";
import router from "@/router";

const API_SERVER = settings.API_SERVER;

export const apiRoutes = {
  user: {
    login: API_SERVER + "auth/token",
    me: API_SERVER + "auth/me",
  },
  lang: {
    list: API_SERVER + "lang/list",
  },
  question: {
    add: API_SERVER + "question",
    update: API_SERVER + "question",
    list: API_SERVER + "question",
    delete: API_SERVER + "question",
  }
};

export function apiCall<T>({ url, method, ...args }: AxiosRequestConfig): Promise<T> {
  return new Promise((resolve, reject) => {
    const token = localStorage.getItem("user-token") || "";

    if (token)
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;

    try {
      axios({
        method: method || "get",
        url: url,
        ...args
      })
        .then(resp => {
          resolve(resp.data);
        })
        .catch(error => {
          console.log(error.response.data.detail)
          if (error.response.data.detail === "Signature has expired") {
            router.push('/')
          } 
          reject(error);
        });
    } catch (err) {
      console.log(err)
      reject(new Error(err));
    }
  })
}

export const fileUpload = ({url, file }: {url: string; file: string}) => 
  new Promise((resolve, reject) => {
    const token = localStorage.getItem("user-token") || "";

    if (token)
      axios.defaults.headers.common["Authorization"] = token;

    const formData = new FormData();
    formData.append('uploadedFile', file);

    try {
      axios.post(url,
          formData,
          {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
        }
      )
      .then(resp => {
        resolve(resp.data);
      })
      .catch(error => {
        reject(error);
      });
    } catch (err) {
      console.log(err)
      reject(new Error(err));
    }
  })