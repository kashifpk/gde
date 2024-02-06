<style scoped>
  .wrapper {
    padding: 0.5em;
    width: 100%;
  }


  label {
    width: 20%;
  }

  input[type=text], select {
    width: 78%
  }
</style>


<template>
  <!--
  name: str
  label: str | None = None
  data_type: str
  content_type: str  # mime type style
  required: bool
  default_value: Any
  -->
  <div class="wrapper">

    <div class="gde-field">
      <label>Name</label>
      <input type="text" />
    </div>

    <div class="gde-field">
      <label>Data type</label>
      <select size="1">
        <option value="text">Text</option>
        <option value="number">number</option>
        <option value="boolean">boolean</option>
        <option value="object">Object/Dict</option>
        <option value="array">array</option>
      </select>
    </div>

    <div class="gde-field">
      <label>Content Type</label>
      <select size="1">
        <option value="text">Text</option>
        <option value="image/icon">Icon</option>
        <option value="image/image">Image</option>
      </select>
    </div>

  </div>

</template>

<script setup>
import { MDBCheckbox } from "mdb-vue-ui-kit";

</script>

