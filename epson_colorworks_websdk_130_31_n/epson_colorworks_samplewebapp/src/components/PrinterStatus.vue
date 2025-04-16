// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div class="PrinterStatus">
    <table width="100%">
      <tbody>
        <tr v-for="(status, index) in statusList" :key="index">
          <th class="label" width="50%">{{ status.name }}:</th>
          <td class="label" width="50%">{{ status.value }}</td>
        </tr>
      </tbody>
    </table>

    <p align="CENTER">
      <button @click="getStatus()">Update</button>
    </p>
  </div>
</template>

<script>
import constdefs from "./constdefs.js";
import { debugLog } from "@/log.js";

export default {
  name: "PrinterStatus",

  props: {
    queueName: {
      type: String,
      default: constdefs.QUEUE_NAME,
    },
  },

  data() {
    return {
      status: {},
    };
  },

  created() {
    this.getStatus();
  },

  computed: {
    statusList() {
      return Object.keys(this.status).map((key) => ({
        name: key,
        value: this.status[key],
      }));
    },
  },

  methods: {
    getStatus() {
      this.axios
        .get(
          [
            constdefs.BACKEND_URL,
            constdefs.API_BASE_PATH,
            this.queueName,
            "printer",
            "status",
          ].join("/")
        )
        .then((response) => {
          this.status = response.data;
          debugLog(this.status);
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