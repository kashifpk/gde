<style>
  /* Component Documentation
  Display data and allow editing the data. Allows dynamically adding and removing fields and JSON view of data.
  */
</style>

<template>

  <MDBRow v-for="field in fields">
    <MDBCol>
      <Field
        :label="field.label || field.name"
        v-model="modelValue[field.name]"
        :initial-mode="props.initialMode"
        :required="field.required || false"
        :choices="field.choices || []" />
    </MDBCol>
  </MDBRow>
</template>

<script setup>

import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"
import { MDBModal, MDBModalHeader, MDBModalTitle, MDBModalBody, MDBModalFooter,
         MDBInput, MDBTextarea, MDBBtn, MDBCol, MDBRow } from "mdb-vue-ui-kit"

import Field from "./Field.vue"

const props = defineProps({
  fields: {
    type: Array
  },
  modelValue: {
    type: Object
  },
  initialMode: {
    type: String,
    default: "view"
  }
})

const emit = defineEmits(['update:modelValue', 'cancel', 'save'])

const nodeKeyTextBox = ref()

const currentMode = ref("view")

onMounted(async () => {
  currentMode.value = props.initialMode
  for(const field of props.fields) {
    if (props.modelValue[field.name] == undefined) {
      console.log(field.name, "has no value set so setting it to null")
      props.modelValue[field.name] = null
    }
  }

  // if(currentMode.value != 'view') {
  //   await nextTick()
  //   // console.log(nodeKeyTextBox.value)
  //   // nodeKeyTextBox.value.inputRef.focus()
  // }
})


</script>



