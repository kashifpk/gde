<template>
  <v-card
    density="comfortable"
    min-width="40vw"
    max-width="80vw"
    prepend-icon="mdi-update"
    title="Add/Update Node"
    elevated
  >
    <v-card-text>
      <DataEditor :fields="editorFields" v-model="fieldsData" initial-mode="edit" />
      <hr />
      <form>
        <label for="extra-info">Extra info</label>
        <Codemirror id="extra-info"
          v-model="extra_info"
          :style="{height: '240px'}"
          :extensions="codemirrorExtensions"
        />
      </form>
    </v-card-text>


    <template v-slot:actions>
      <v-spacer></v-spacer>
      <v-btn size="large" :prepend-icon="mdiCloseCircle" @click="$emit('cancel')">
        <template v-slot:prepend>
          <v-icon color="danger"></v-icon>
        </template>
        Cancel
      </v-btn>
      <v-btn size="large" :prepend-icon="mdiCheckCircle" @click="save()">
        <template v-slot:prepend>
          <v-icon color="success"></v-icon>
        </template>
        Save
      </v-btn>
    </template>
  </v-card>

</template>

<script setup lang="ts">

  import axios from "axios"
  import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"
  import { mdiCheckCircle, mdiCloseCircle } from '@mdi/js'

  import { Codemirror } from "vue-codemirror"
  import { json } from "@codemirror/lang-json"
  import { python } from "@codemirror/lang-python"
  import { oneDark } from "@codemirror/theme-one-dark"

  import type {FieldSpecification, FieldsData} from "../type_defs.ts"
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
  const fieldsData = ref<FieldsData>({})
  const nodeTypes = ref({})
  const nodeTypeNames = ref([])
  const editorFields = ref<FieldSpecification[]>([])


  onMounted(async () => {
    fieldsData.value = {...props.modelValue}

    extra_info.value = JSON.stringify(props.modelValue.extra_info, null, 2)
    console.log("model value:", props.modelValue)

    // set nodeTypes.value to only those nodes in store.nodeTypes where is_edge is true
    let is_edge = props.nodeType == "edge"
    for(let nodeType in store.nodeTypes) {
      if(store.nodeTypes[nodeType].is_edge == is_edge) {
        nodeTypes.value[nodeType] = store.nodeTypes[nodeType]
      }
    }

    nodeTypeNames.value = Object.keys(nodeTypes.value)
    updateFieldsData()
    buildEditorFields()

  })

  watch(
    fieldsData,
    () => {
      buildEditorFields()
    },
    { deep: true }
  )

  const updateFieldsData = () => {
    // set the label and node type fields for DataEditor
    fieldsData.value.label = fieldsData.value._meta.label == undefined ? "" : fieldsData.value._meta.label
    fieldsData.value.node_type = fieldsData.value._meta.node_type == undefined ? "" : fieldsData.value._meta.node_type
  }

  const buildEditorFields = () => {
    // empty editorFields.value array
    editorFields.value = []

    editorFields.value.push({name: '_key', label: "Key", data_type: "string", required: true})
    if (props.nodeType == 'edge') {
      editorFields.value.splice(1, 0, {name: 'source', data_type: "string", label: "Source", value: props.modelValue['source'], required: true});
      editorFields.value.splice(2, 0, {name: 'target', data_type: "string", label: "Target", value: props.modelValue['target'], required: true});
    }
    editorFields.value.push({name: 'node_type', data_type: "string", label: 'Type', choices: nodeTypeNames.value})

    if(fieldsData.value.node_type == "" || fieldsData.value.node_type == undefined)
      editorFields.value.push({name: 'label', data_type: "string", label: "Node Label"})
    else {
      // add fields from nodeTypes.value.fields for the current selected node into editorFields
      console.log("trying to add fields based on node type")
      console.log(fieldsData.value.node_type)
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

