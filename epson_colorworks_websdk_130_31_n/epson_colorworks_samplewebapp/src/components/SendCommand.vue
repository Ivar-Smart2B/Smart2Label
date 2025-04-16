// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div id="sendcommand">
    <table align="center">
      <thead>
        <tr>
          <th class="label">
            <a name="SendCommand">Send Command</a>
          </th>
          <th>--></th>
          <th class="label">
            <a name="Response">Response</a>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <input type="file" v-on:change="didChangeCommandFile" />
          </td>
          <td></td>
          <td>
            <div>
              <input type="checkbox" v-model="requiresResponse" /><label
                >Requires response</label
              >
            </div>
            <a
              v-bind:href="responseURL"
              download="response.dat"
              ref="download_link"
              >{{ message }}</a
            >
          </td>
        </tr>
      </tbody>
    </table>

    <p align="center">
      <button v-bind:disabled="!isSendable" v-on:click="sendCommand()">
        Send
      </button>
    </p>
  </div>
</template>


<script>
import constdefs from "./constdefs.js";
import { debugLog } from "@/log.js";

export default {
  name: "SendCommand",

  props: {
    queueName: {
      type: String,
      default: constdefs.QUEUE_NAME,
    },
  },

  data() {
    return {
      commandFile: null,
      response: null,
      requiresResponse: false,
    };
  },

  computed: {
    isSendable() {
      return this.commandFile != null;
    },

    responseURL() {
      if (this.response != null) {
        return URL.createObjectURL(this.response);
      } else {
        return null;
      }
    },

    message() {
      if (this.response != null) {
        return "Download";
      } else {
        return "";
      }
    },
  },

  methods: {
    toBlob(base64, mime_ctype) {
      var bom = new Uint8Array();

      var bin = atob(base64.replace(/^.*,/, ""));
      var buffer = new Uint8Array(bin.length);
      for (var i = 0; i < bin.length; i++) {
        buffer[i] = bin.charCodeAt(i);
      }

      try {
        var blob = new Blob([bom, buffer.buffer], {
          type: mime_ctype,
        });
      } catch (e) {
        return false;
      }
      return blob;
    },

    didChangeCommandFile(e) {
      this.commandFile = e.target.files[0];
      debugLog(this.commandFile);
    },

    sendCommand() {
      this.response = null;

      const reader = new FileReader();
      reader.onload = (e) => {
        let request = {
          command: e.target.result,
          requiresResponse: this.requiresResponse,
        };

        debugLog(request);

        this.axios
          .post(
            [
              constdefs.BACKEND_URL,
              constdefs.API_BASE_PATH,
              this.queueName,
              "printer",
              "sendcommand",
            ].join("/"),
            request
          )
          .then((response) => {
            debugLog(response);
            this.response = this.toBlob(
              response.data,
              "application/octet-stream"
            );
          })
          .then(() => {
            const elem = this.$refs.download_link;
            elem.click();
          })
          .catch((error) => {
            window.alert(error);
          });
      };
      reader.readAsDataURL(this.commandFile);
    },
  },
};
</script>


<style scoped>
td {
  text-align: center;
}

TH.label {
  text-align: center;
  vertical-align: top;
  font-weight: bold;
}
</style>