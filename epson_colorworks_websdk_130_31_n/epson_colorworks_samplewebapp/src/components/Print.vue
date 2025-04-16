// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div id="print">
    <table width="100%">
      <tbody>
        <tr>
          <th class="label" width="50%">
            <a name="PrintImageFile">Print Image File</a>:
          </th>
          <td>
            <input type="file" v-on:change="didChangePrintFile" />
          </td>
        </tr>

        <tr>
          <th class="label" width="50%"><a name="Copies">Copies</a>:</th>
          <td>
            <input
              type="number"
              v-model="copies"
              :max="copiesRange.max"
              :min="copiesRange.min"
              :step="copiesRange.step"
              @change="didChangeCopies"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <p align="CENTER">
      <button v-bind:disabled="!isPrintable" v-on:click="sendPrintData()">
        Print
      </button>
    </p>
  </div>
</template>


<script>
import constdefs from "./constdefs.js";
import { debugLog } from "@/log.js";

export default {
  name: "Print",

  props: {
    queueName: {
      type: String,
      default: constdefs.QUEUE_NAME,
    },
  },

  data() {
    return {
      printImageFile: null,
      copies: 1,
    };
  },

  computed: {
    isPrintable() {
      return this.printImageFile != null;
    },

    copiesRange() {
      return {
        min: 1,
        max: 100,
        step: 1,
      }
    },
  },

  methods: {
    didChangePrintFile(e) {
      this.printImageFile = e.target.files[0];
      debugLog(this.printImageFile);
    },

    didChangeCopies() {
      let newValue = this.copies;
      const min = this.copiesRange.min;
      const max = this.copiesRange.max;

      this.copies = Math.min(max, Math.max(min, newValue));
    },

    sendPrintData() {
      const reader = new FileReader();
      reader.onload = (e) => {
        let request = {
          "mime-type": this.printImageFile.type,
          image: e.target.result,
          copies: this.copies,
        };

        debugLog(request);

        this.axios
          .post(
            [
              constdefs.BACKEND_URL,
              constdefs.API_BASE_PATH,
              this.queueName,
              "print",
            ].join("/"),
            request
          )
          .then((response) => {
            debugLog(response);
          })
          .catch((error) => {
            window.alert(error);
          });
      };
      reader.readAsDataURL(this.printImageFile);
    },
  },
};
</script>


<style scoped>
</style>