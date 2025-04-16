// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div class="PrinterInfo">
    <table width="100%">
      <tbody>
        <tr v-for="(info, index) in infoList" :key="index">
          <th class="label" width="50%">{{ info.name }}:</th>
          <td class="label" width="50%">{{ info.value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import constdefs from "./constdefs.js";
import { debugLog } from "@/log.js";

export default {
  name: "PrinterInfo",

  props: {
    queueName: {
      type: String,
      default: constdefs.QUEUE_NAME,
    },
  },

  data() {
    return {
      info: {},
    };
  },

  computed: {
    infoList() {
      return Object.keys(this.info).map((key) => ({
        name: key,
        value: this.info[key],
      }));
    },
  },

  created() {
    this.getInfo();
  },

  methods: {
    getInfo() {
      this.axios
        .get(
          [
            constdefs.BACKEND_URL,
            constdefs.API_BASE_PATH,
            this.queueName,
            "printer",
            "info",
          ].join("/")
        )
        .then((response) => {
          this.info = response.data;
          debugLog(this.info);
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