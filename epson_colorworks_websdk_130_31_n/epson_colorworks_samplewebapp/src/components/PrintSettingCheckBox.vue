// 
// Epson Label Printer Web SDK Sample Web App
//
// Created by Seiko Epson Corporation on 2021/9/8.
// Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
// 

<template>
  <label>
    <input type="checkbox" v-model="selectedValue" @change="didChangeValue" />
    {{ label }}
  </label>
</template>


<script>
export default {
  name: "PrintSettingCheckBox",

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
