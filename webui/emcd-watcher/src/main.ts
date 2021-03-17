import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { store } from './store'
import 'izitoast/dist/css/iziToast.min.css';
import Datepicker from 'vue3-datepicker'

createApp(App)
    .use(store)
    .use(router)
    .component('datepicker', Datepicker)
    .mount('#app')
