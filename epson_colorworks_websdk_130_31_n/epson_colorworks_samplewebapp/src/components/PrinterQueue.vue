// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div id="PrinterQueue">
    <table width="100%">
      <tbody>
        <tr>
          <th class="label" width="50%">
            <a name="PrinterQueue">Printer Queue</a>:
          </th>
          <td>
            <div v-show="hasQueue">
              <select v-model="selectedQueueName" @change="didChangePrinter">
                <option
                  v-for="(queueName, index) in printerQueue"
                  :key="index"
                  :value="queueName"
                >
                  {{ queueName }}
                </option>
              </select>
            </div>

            <div v-show="!hasQueue">
              Not found
            </div>

          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import constdefs from "./constdefs.js";
import { debugLog } from "@/log.js";

export default {
  name: "PrinterQueue",

  porps: {
    queueName: String,
  },

  data() {
    return {
      printerQueue: null,
      selectedQueueName: this.queueName,
    };
  },

  computed: {
    hasQueue() {
      return this.printerQueue && this.printerQueue.length > 0;
    },
  },

  mounted() {
    this.getPrinterQueue();
  },

  methods: {
    getPrinterQueue() {
      this.axios
        .get([constdefs.BACKEND_URL, constdefs.API_BASE_PATH, "list"].join("/"))
        .then((response) => {
          this.printerQueue = response.data;
          debugLog(this.printerQueue);

          if (this.selectedQueueName == null) {
            this.selectedQueueName = this.printerQueue[0];
            this.didChangePrinter();
          }
        })
        .catch((error) => {
          window.alert(error);
        });
    },

    didChangePrinter() {
      debugLog(this.selectedQueueName);
      this.$emit("update:queueName", this.selectedQueueName);
    },
  },
};
</script>


<style scoped>
</style>