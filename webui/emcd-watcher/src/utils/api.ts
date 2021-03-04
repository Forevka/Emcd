import axios, { AxiosRequestConfig } from "axios";
import { settings } from "@/settings";

const API_SERVER = settings.API_SERVER;

export const apiRoutes = {
  user: {
    login: API_SERVER + "auth/token",
  },
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