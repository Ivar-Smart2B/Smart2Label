// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div id="cancel">
    <p align="CENTER">
      <button v-on:click="cancelJob()">
        Cancel Job
      </button>
    </p>
  </div>
</template>


<script>
import constdefs from "./constdefs.js";
import { debugLog } from "@/log.js";

export default {
  name: "Cancel",

  props: {
    queueName: {
      type: String,
      default: constdefs.QUEUE_NAME,
    },
  },

  methods: {
    cancelJob() {
      this.axios
        .get(
          [
            constdefs.BACKEND_URL,
            constdefs.API_BASE_PATH,
            this.queueName,
            "print",
            "cancel",
          ].join("/")
        )
        .then((response) => {
          debugLog(response);
        })
        .catch((error) => {
          window.alert(error);
        });
    },
  },
};
</script>


<style scoped>
</style>