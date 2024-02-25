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
        v-model="extra_info"
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

import axios from "axios"
import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"
import { MDBModal, MDBModalHeader, MDBModalTitle, MDBModalBody, MDBModalFooter,
         MDBInput, MDBTextarea, MDBBtn, MDBCol, MDBRow } from "mdb-vue-ui-kit"
import { Codemirror } from "vue-codemirror"
import { json } from "@codemirror/lang-json"
import { python } from "@codemirror/lang-python"
import { oneDark } from "@codemirror/theme-one-dark"

import { useStore } from '../store.ts'
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
const store = useStore()
const extra_info = ref("")
const fieldsData = ref({})
const nodeTypes = ref({})
const nodeTypeNames = ref([])
const editorFields = ref([])
const haveLabel = ref(false)


onMounted(async () => {
  fieldsData.value = {...props.modelValue}
  if (props.nodeType == 'edge') {
    editorFields.value.splice(1, 0, {name: 'source', label: "Source", value: props.modelValue['source'], required: true});
    editorFields.value.splice(2, 0, {name: 'target', label: "Target", value: props.modelValue['target'], required: true});
  }
  extra_info.value = JSON.stringify(props.modelValue.extra_info, null, 2)
  console.log("model value:", props.modelValue)

  nodeTypes.value = store.nodeTypes
  nodeTypeNames.value = Object.keys(nodeTypes.value)
  updateFieldsData()
  buildEditorFields()

})

watch(
  fieldsData,
  () => {

    updateEditorFields()
  },
  { deep: true }
)

const updateFieldsData = () => {
  fieldsData.value.label = fieldsData.value._meta.label == undefined ? "" : fieldsData.value._meta.label
  fieldsData.value.node_type = fieldsData.value._meta.node_type == undefined ? "" : fieldsData.value._meta.node_type
}

const buildEditorFields = () => {
  console.log("buildEditorFields", editorFields.value)
  editorFields.value.push({name: '_key', label: "Key", required: true})
  editorFields.value.push({name: 'node_type', label: 'Type', choices: nodeTypeNames.value})
  updateEditorFields()
}

const updateEditorFields = () => {
  // update editor fields when node type is changed adding/removing fields for that node.
  console.log("updateEditorFields", fieldsData.value, editorFields.value)
  if(fieldsData.value.node_type == "" && haveLabel.value == false) {
    fieldsData.value.label = ""
    editorFields.value.push({name: 'label', label: "Node Label"})
    haveLabel.value = true
  }

  if(fieldsData.value.node_type != "" && haveLabel.value == true) {
    // find object in editosFields.value array and remove it
    const index = editorFields.value.findIndex(obj => obj.name === 'label')
    // remove element in editorFields.value array at index
    editorFields.value.splice(index, 1)

    delete fieldsData.value.label
    haveLabel.value = false

    // add fields from nodeTypes.value.fields for the current selected node into editorFields
    nodeTypes.value[fieldsData.value.node_type].fields.forEach(field => {
      editorFields.value.push(field)
    })
  }

}

const getMetaLabel = () => {
  if (fieldsData.value.label)
    return fieldsData.value.label

  if (fieldsData.value.node_type) {
    if (fieldsData.value[store.nodeTypes[fieldsData.value.node_type].label_field])
      return fieldsData.value[store.nodeTypes[fieldsData.value.node_type].label_field]
  }

  return fieldsData.value._key
}

const save = () => {
  if (extra_info.value) {
    console.log("have extra info")
    fieldsData.value.extra_info = JSON.parse(extra_info.value)
  }
  console.log("fieldsData on save", fieldsData.value)
  let meta = {
    label: getMetaLabel(),
    node_type: fieldsData.value.node_type,
    display_type: fieldsData.value.node_type ? store.nodeTypes[fieldsData.value.node_type].default_display_type : null,
    display_value: fieldsData.value.node_type ? store.nodeTypes[fieldsData.value.node_type].default_display_value : null
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

