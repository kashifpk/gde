import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getNodeTypes } from './graph_nodes_utils'

export const useStore = defineStore('gde', () => {
  const nodeTypes = ref({})

  async function loadNodeTypes() {
    nodeTypes.value = await getNodeTypes()
  }

  return { nodeTypes, loadNodeTypes }
})
