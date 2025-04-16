// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <input
    type="number"
    v-model="selectedValue"
    :min="min"
    :max="max"
    :step="capability.step"
    @change="didChangeValue"
  />
</template>


<script>
export default {
  name: "PrintSettingNumberBox",

  props: ["capability", "value", "label"],

  data() {
    return {
      selectedValue: this.value,
    };
  },

  computed: {
    min() {
      return this.findMinValFromCap(this.capability.min);
    },

    max() {
      return this.findMaxValFromCap(this.capability.max);
    },
  },

  mounted() {
    this.selectedValue = this.capability.current;
    this.didChangeValue();
  },

  methods: {
    findMinValFromCap(cap) {
      if (typeof(cap) === "object") {
        return Math.min(...Object.values(cap));
      } else {
        return cap;
      }
    },

    findMaxValFromCap(cap) {
      if (typeof(cap) === "object") {
        return Math.max(...Object.values(cap));
      } else {
        return cap;
      }
    },

    didChangeValue() {
      let newValue = this.selectedValue;
      const min = this.min;
      const max = this.max;

      this.selectedValue = Math.min(max, Math.max(min, newValue));
      this.$emit("update:value", Number(this.selectedValue));
    },
  },
};
</script>
