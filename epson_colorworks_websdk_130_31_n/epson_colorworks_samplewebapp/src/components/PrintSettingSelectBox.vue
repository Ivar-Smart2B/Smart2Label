// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <select v-model="selectedValue" @change="didChangeValue">
    <option
      v-for="(value, index) in capability.values"
      :key="index"
      :value="value"
    >
      {{ value }}
    </option>
  </select>
</template>


<script>
export default {
  name: "PrintSettingSelectBox",

  props: ["capability", "value", "label"],

  data() {
    return {
      selectedValue: this.value,
    };
  },

  mounted() {
    this.selectedValue = this.capability.current;
    this.didChangeValue();
  },

  methods: {
    didChangeValue() {
      this.$emit("update:value", this.selectedValue);
    },
  },
};
</script>
