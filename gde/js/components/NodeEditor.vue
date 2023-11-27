<template>
  <MDBModalHeader>
    <MDBModalTitle> Add Node </MDBModalTitle>
  </MDBModalHeader>

  <MDBModalBody>
    <form>
      <template v-if="mode=='update'">
        <MDBRow>
          <MDBCol col="3">Key</MDBCol>
          <MDBCol col="9">{{ modelValue._key }}</MDBCol>
        </MDBRow>
        <MDBRow v-if="nodeType=='edge'">
          <MDBCol col="3">Source</MDBCol>
          <MDBCol col="9">{{ modelValue.source }}</MDBCol>
        </MDBRow>
        <MDBRow v-if="nodeType=='edge'">
          <MDBCol col="3">Target</MDBCol>
          <MDBCol col="9">{{ modelValue.target }}</MDBCol>
        </MDBRow>
      </template>
      <template v-else>
        <MDBInput ref="nodeKeyTextBox" label="Key" v-model="modelValue._key" class="mb-4" />
        <MDBInput v-if="nodeType=='edge'" label="Source" v-model="modelValue.source" class="mb-4" />
        <MDBInput v-if="nodeType=='edge'" label="Target" v-model="modelValue.target" class="mb-4" />
      </template>

      <MDBInput label="Node Label" v-model="modelValue.label" class="mb-4" />

      <!-- <MDBTextarea label="Extra Info (JSON)" rows="4" v-model="modelValue.extraInfo" class="mb-4" /> -->
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

const nodeKeyTextBox = ref()
const extraInfo = ref("")

onMounted(async () => {
  if(props.mode == 'new') {
    await nextTick()
    // console.log(nodeKeyTextBox.value)
    nodeKeyTextBox.value.inputRef.focus()
  }

  extraInfo.value = JSON.stringify(props.modelValue.extraInfo, null, 2)
})

const save = () => {
  console.log(extraInfo.value)
  if (extraInfo.value) {
    props.modelValue.extraInfo = JSON.parse(extraInfo.value)
  }
  emit('update:modelValue', props.modelValue)
  emit('save')
}


</script>

<style>

</style>

