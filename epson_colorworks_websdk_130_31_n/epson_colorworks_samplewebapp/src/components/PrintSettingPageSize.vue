// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <div>
    <select v-model="selectedValue" @change="didChangeValue">
      <option
        v-for="(value, index) in capability.values"
        :key="index"
        :value="value"
      >
        {{ value }}
      </option>
    </select>

    <table v-show="isCustom">
      <tbody>
        <tr>
          <th class="label">Width:</th>
          <td>
            <input
              type="number"
              v-model="customWidth"
              :max="maxCustomWidth"
              :min="minCustomWidth"
              :step="0.1"
              @change="didChangeValue"
            />
            mm
          </td>
        </tr>
        <tr>
          <th class="label">Height:</th>
          <td>
            <input
              type="number"
              v-model="customHeight"
              :max="maxCustomHeight"
              :min="minCustomHeight"
              :step="0.1"
              @change="didChangeValue"
            />
            mm
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
const CUSTOM_PAGESIZE_ITEM = "Custom.WIDTHxHEIGHT";

export default {
  name: "PrintSettingPageSize",

  props: ["capability", "value", "label"],

  data() {
    return {
      selectedValue: null,

      customWidth: 0,
      customHeight: 0,
    };
  },

  computed: {
    isCustom() {
      return this.selectedValue == CUSTOM_PAGESIZE_ITEM;
    },

    minCustomWidth() {
      return this.findMinValFromCustomCap(this.capability.customwidth.min);
    },
    maxCustomWidth() {
      return this.findMaxValFromCustomCap(this.capability.customwidth.max);
    },

    minCustomHeight() {
      return this.findMinValFromCustomCap(this.capability.customheight.min);
    },
    maxCustomHeight() {
      return this.findMaxValFromCustomCap(this.capability.customheight.max);
    },
  },

  mounted() {
    if (typeof this.capability.current === "object") {
      this.selectedValue = CUSTOM_PAGESIZE_ITEM;
      this.customWidth = this.capability.current.CustomWidth;
      this.customHeight = this.capability.current.CustomHeight;
    } else {
      this.selectedValue = this.capability.current;
    }
    this.didChangeValue();
  },

  methods: {
    findMinValFromCustomCap(customCap) {
      if (typeof(customCap) === "object") {
        return Math.min(...Object.values(customCap));
      } else {
        return customCap;
      }
    },

    findMaxValFromCustomCap(customCap) {
      if (typeof(customCap) === "object") {
        return Math.max(...Object.values(customCap));
      } else {
        return customCap;
      }
    },

    didChangeValue() {
      if (this.isCustom) {
        let newW = this.customWidth;
        const minW = this.minCustomWidth;
        const maxW = this.maxCustomWidth;
        this.customWidth = Math.min(maxW, Math.max(minW, newW));

        let newH = this.customHeight;
        const minH = this.minCustomHeight;
        const maxH = this.maxCustomHeight;
        this.customHeight = Math.min(maxH, Math.max(minH, newH));

        let dict = {
          CustomWidth: Number(this.customWidth),
          CustomHeight: Number(this.customHeight),
        };
        this.$emit("update:value", dict);
      } else {
        this.$emit("update:value", this.selectedValue);
      }
    },
  },
};
</script>
