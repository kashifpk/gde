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


    <!-- <MDBCol col="3">{{ field.label || field.name }}</MDBCol>
    <MDBCol col="9">{{ field.value || '' }}</MDBCol> -->
  </MDBRow>

</template>

<script setup>

import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"
import { MDBModal, MDBModalHeader, MDBModalTitle, MDBModalBody, MDBModalFooter,
         MDBInput, MDBTextarea, MDBBtn, MDBCol, MDBRow } from "mdb-vue-ui-kit"
import { Codemirror } from "vue-codemirror"
import { json } from "@codemirror/lang-json"
import { python } from "@codemirror/lang-python"
import { oneDark } from "@codemirror/theme-one-dark"

import Field from "./Field.vue"

const props = defineProps({
  fields: {
    type: Array
  },
  allowExtraFields: {
    type: Boolean,
    default: true
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

const codemirrorExtensions = [json(), python(), oneDark]

const nodeKeyTextBox = ref()
const extraInfo = ref("")
const currentMode = ref("view")

onMounted(async () => {
  console.log(props.modelValue)
  currentMode.value = props.initialMode
  for(const field of props.fields) {
    if(props.modelValue.hasOwnProperty(field.name))
      continue

    props.modelValue[field.name] = field.value ?? null
    // console.log(field.name)
  }

  // if(currentMode.value != 'view') {
  //   await nextTick()
  //   // console.log(nodeKeyTextBox.value)
  //   // nodeKeyTextBox.value.inputRef.focus()
  // }
})

// const save = () => {
//   console.log(extraInfo.value)
//   if (extraInfo.value) {
//     props.modelValue.extraInfo = JSON.parse(extraInfo.value)
//   }
//   emit('update:modelValue', props.modelValue)
//   emit('save')
// }


</script>



