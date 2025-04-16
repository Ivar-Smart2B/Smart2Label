// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div id="app">
    <h1>Web SDK Sample App</h1>

    <printer-queue :queueName.sync="syncedQueueName" />

    <hr />

    <div v-show="isReady">
      <p align="CENTER">
        <select v-model="currentView">
          <option
            v-for="(view, index) in views"
            :key="index"
            :value="view.class"
          >
            {{ view.text }}
          </option>
        </select>
      </p>
      <hr />

      <component v-if="queueName" :is="currentView" v-bind="childProps" />
    </div>

    <div v-show="!isReady">
      Printer queue not found. Add printer to CUPS server then reload.
    </div>
  </div>
</template>

<script>
import PrinterQueue from "./components/PrinterQueue.vue";
import PrinterInfo from "./components/PrinterInfo.vue";
import PrinterStatus from "./components/PrinterStatus.vue";
import PrinterSetting from "./components/PrinterSetting.vue";
import PrintSetting from "./components/PrintSetting.vue";
import Print from "./components/Print.vue";
import SendCommand from "./components/SendCommand.vue";

export default {
  name: "App",
  components: {
    PrinterQueue,
    PrinterInfo,
    PrinterStatus,
    PrintSetting,
    PrinterSetting,
    Print,
    SendCommand,
  },

  data() {
    return {
      queueName: null,
      currentView: PrintSetting,
      views: [
        { text: "Printer Info", class: PrinterInfo },
        { text: "Printer Status", class: PrinterStatus },
        { text: "Printer Setting", class: PrinterSetting },
        { text: "Print Setting", class: PrintSetting },
        { text: "Print", class: Print },
        { text: "Send Command", class: SendCommand },
      ],
    };
  },

  computed: {
    isReady() {
      return this.queueName != null;
    },

    childProps() {
      if (this.queueName != null) {
        return { queueName: this.queueName };
      } else {
        return null;
      }
    },

    syncedQueueName: {
      get: function () {
        return this.queueName;
      },
      set: function (val) {
        this.queueName = null;

        new Promise((resolve) => {
          resolve();
        }).then(() => {
          this.queueName = val;
        });
      },
    },
  },
};
</script>

<style>
#app {
  text-align: center;
}

TH.label {
  text-align: right;
  vertical-align: top;
  font-weight: normal;
}

td {
  text-align: left;
}
</style>
