<template>
  <MDBModalHeader>
    <MDBModalTitle> Add Node </MDBModalTitle>
  </MDBModalHeader>

  <MDBModalBody>
    <DataEditor :fields="editorFields" v-model="fieldsData" initial-mode="edit" />
    <hr />
    <form>
      <label for="extra-info">Extra info</label>
      <Codemirror id="extra-info"
        v-model="extraInfo"
        :style="{height: '400px'}"
        :extensions="codemirrorExtensions"
      />
  </form>
  </MDBModalBody>
  <MDBModalFooter>
    <MDBBtn color="secondary" @click="$emit('cancel')">Cancel</MDBBtn>
    <MDBBtn color="primary" @click="save()">Save changes</MDBBtn>
  </MDBModalFooter>

</template>

<script setup>

import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"
import { MDBModal, MDBModalHeader, MDBModalTitle, MDBModalBody, MDBModalFooter,
         MDBInput, MDBTextarea, MDBBtn, MDBCol, MDBRow } from "mdb-vue-ui-kit"
import { Codemirror } from "vue-codemirror"
import { json } from "@codemirror/lang-json"
import { python } from "@codemirror/lang-python"
import { oneDark } from "@codemirror/theme-one-dark"

import DataEditor from "./DataEditor.vue"

const props = defineProps({
  modelValue: {
    type: Object
  },
  mode: {
    type: String,
    required: true,
  },
  nodeType: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'cancel', 'save'])

const codemirrorExtensions = [json(), python(), oneDark]

// const nodeKeyTextBox = ref()
const extraInfo = ref("")
const fieldsData = ref({})
const editorFields = ref([
  {name: '_key', label: "Key", required: true},
  {name: 'node_type', label: 'Type', choices: ["person", "event"]},
  {name: 'label', label: "Node Label"},
  {name: 'name', value: 'Anonymous'}
])

onMounted(async () => {
  fieldsData.value = {...props.modelValue}
  if (props.nodeType == 'edge') {
    editorFields.value.splice(1, 0, {name: 'source', label: "Source", value: props.modelValue['source'], required: true});
    editorFields.value.splice(2, 0, {name: 'target', label: "Target", value: props.modelValue['target'], required: true});
  }
  extraInfo.value = JSON.stringify(props.modelValue.extraInfo, null, 2)
  console.log("model value:", props.modelValue)
  console.log(fieldsData.value._meta.label)
  fieldsData.value.label = fieldsData.value._meta.label
  fieldsData.value.node_type = fieldsData.value._meta.node_type
})

const save = () => {
  if (extraInfo.value) {
    console.log("have extra info")
    fieldsData.value.extraInfo = JSON.parse(extraInfo.value)
  }
  console.log("fieldsData on save", fieldsData.value)
  const meta = {
    label: fieldsData.value.label,
    node_type: fieldsData.value.node_type
  }

  fieldsData.value._meta = {...meta}
  delete fieldsData.value.label
  delete fieldsData.value.node_type
  console.log(fieldsData.value)
  emit('update:modelValue', fieldsData.value)
  emit('save')
}


</script>

<style>

</style>

