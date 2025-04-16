// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div class="PrintSetting" v-if="isShown">
    <table width="100%">
      <tbody>
        <tr v-for="(capability, index) in capabilities" :key="index">
          <th class="label" width="50%">{{ capability.name }}:</th>
          <td>
            <component
              :is="componentNames[capability.name]"
              :capability="capability"
              :value.sync="printSetting[capability.name]"
              :label="capability.name"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <p align="CENTER">
      <button @click="sendPrintSettings()">Set</button>
    </p>
  </div>
</template>

<script>
import constdefs from "./constdefs.js";
import PrintSettingSelectBox from "./PrintSettingSelectBox.vue";
import PrintSettingCheckBox from "./PrintSettingCheckBox.vue";
import PrintSettingNumberBox from "./PrintSettingNumberBox.vue";
import PrintSettingPageSize from "./PrintSettingPageSize.vue";
import { debugLog } from "@/log.js";

export default {
  name: "PrintSetting",

  components: {
    PrintSettingSelectBox,
    PrintSettingCheckBox,
    PrintSettingNumberBox,
    PrintSettingPageSize,
  },

  props: {
    queueName: {
      type: String,
      default: constdefs.QUEUE_NAME,
    },
  },

  data() {
    return {
      capabilities: [],
      printSetting: {},
      isShown: true,
    };
  },

  computed: {
    componentNames() {
      let dict = {};
      for (const value of this.capabilities) {
        const key = value.name;

        dict[key] = ((capability) => {
          if (capability.type == "pagesize") {
            return PrintSettingPageSize;
          }

          switch (capability.capabilitytype) {
            case "array":
              return PrintSettingSelectBox;
            case "boolean":
              return PrintSettingCheckBox;
            case "range":
              return PrintSettingNumberBox;
          }
        })(value);
      }
      return dict;
    },
  },

  mounted() {
    this.getCapability();
  },

  methods: {
    getCapability() {
      this.axios
        .get(
          [
            constdefs.BACKEND_URL,
            constdefs.API_BASE_PATH,
            this.queueName,
            "print",
            "capability",
          ].join("/")
        )
        .then((response) => {
          this.capabilities = response.data;
          debugLog(this.capabilities);
        })
        .catch((error) => {
          window.alert(error);
        });
    },

    sendPrintSettings() {
      debugLog(this.printSetting);

      this.isShown = false;

      this.axios
        .post(
          [
            constdefs.BACKEND_URL,
            constdefs.API_BASE_PATH,
            this.queueName,
            "print",
            "setting",
          ].join("/"),
          this.printSetting
        )
        .then((response) => {
          debugLog(response);
          this.capabilities = response.data;
        })
        .catch((error) => {
          window.alert("Error status " + error.response.status + ": " + error.response.data.message);
        })
        .finally(() => {
          this.isShown = true;
        });
    },
  },
};
</script>

<style scoped>
</style>