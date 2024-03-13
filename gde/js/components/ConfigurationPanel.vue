<style scoped>

  .panel {
    position: absolute;
    left: 99.8%;
    top: 7vh;
    z-index: 1;
    column-gap: 1vh;
    width: 1%;
    height: 400px;
    transform: rotate(90deg);
    transform-origin: left top 0;
  }

  .panel .tab {
    padding-left: 1vh;
    padding-right: 1vh;
    border: 1px solid #a6a6a6;
    color: #ffffff;
    background-color: #151515;
    white-space: nowrap;
  }

  .panel .tab-active {
    background-color: #4b4a4a;
  }

  .panel .tab:hover {
    background-color: #4b4a4a;
    cursor: pointer;
  }

  .panel-content {
    border: 4px solid #a6a6a6;
    border-radius: 1vh;
    color: #ffffff;
    background-color: #272127;
    min-height: 30%;
    position: absolute;
    width: 40%;
    left: 57.5%;
    top: 8vh;
    z-index: 1;
    height: 70vh;

  }

  .panel-title {
    background-color: #242424;
    height: 6vh;
    padding: 6px;
    border-bottom: solid #4b4a4a;
  }

</style>

<template>
  <div class="panel">
    <span class="tab" :class="{'tab-active': isPanelOpen && activePanel == 'Field Manager'}" @click="loadPanel('Field Manager')">
      Field Manager
    </span>
    <span class="tab" :class="{'tab-active': isPanelOpen && activePanel == 'Node Manager'}" @click="loadPanel('Node Manager')">
      Node Manager
    </span>

  </div>
  <div v-if="isPanelOpen" class="panel-content">
    <div class="panel-title">
      {{ activePanel }}
      <v-btn class="float-right" :icon="mdiChevronRight" color="link" title="Collapse" @click="collapsePanel()">
      </v-btn>
    </div>

    <NodeTypeManager v-if="activePanel == 'Node Manager'"></NodeTypeManager>
    <FieldManager v-if="activePanel == 'Field Manager'"></FieldManager>

  </div>

</template>

<script setup>

import { onMounted, computed, ref, reactive, watch, nextTick} from "vue"
import {mdiChevronRight} from "@mdi/js"
import NodeTypeManager from "./NodeTypeManager.vue"
import FieldManager from "./FieldManager.vue"

// const props = defineProps({
//   modelValue: {
//     type: Object
//   },
//   mode: {
//     type: String,
//     required: true,
//   },
//   nodeType: {
//     type: String,
//     required: true
//   }
// })

// const emit = defineEmits(['update:modelValue', 'cancel', 'save'])

const isPanelOpen = ref(false)
const activePanel = ref("")

onMounted(async () => {
  // if(props.mode == 'new') {
  //   await nextTick()
  //   // console.log(nodeKeyTextBox.value)
  //   nodeKeyTextBox.value.inputRef.focus()
  // }

  // extraInfo.value = JSON.stringify(props.modelValue.extraInfo, null, 2)
})

const loadPanel = (panelName) => {
  isPanelOpen.value = true
  activePanel.value = panelName
  console.log(panelName)
}

const collapsePanel = () => {
  isPanelOpen.value = false
}

const save = () => {
  // console.log(extraInfo.value)
  // if (extraInfo.value) {
  //   props.modelValue.extraInfo = JSON.parse(extraInfo.value)
  // }
  // emit('update:modelValue', props.modelValue)
  // emit('save')
}


</script>



