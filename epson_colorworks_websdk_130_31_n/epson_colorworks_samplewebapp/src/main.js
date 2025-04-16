// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false

Vue.use(VueAxios, axios);

new Vue({
  render: h => h(App),
}).$mount('#app')
