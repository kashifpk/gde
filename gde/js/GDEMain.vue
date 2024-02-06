<style>
.graph {
  border: 1px solid #837f7f;
  height: 89vh;

}

#graph-div {
  width: 99%;
  margin-top: 5vh;

}

.v-ng-container {
  background-color: #1b1b1b;
}
.add-edge-div {
  border: 1px solid #1d1f22;
  padding: 10px;
}

.status {
  border-top: 2px solid #1b1b1b;
}

</style>

<template>
  <MDBNavbar dark bg="dark" position="top" container classContainer="justify-content-start">
    <MDBNavbarBrand>
      <MDBIcon icon="share-nodes" size="1x" />
    </MDBNavbarBrand>

    <MDBNavbarNav class="d-flex flex-row">
      <MDBNavbarItem class="me-3 me-lg-0 ps-2">
        <MDBBtn outline="light" floating title="New graph" @click="newGraph()">
          <MDBIcon icon="file"></MDBIcon>
        </MDBBtn>
      </MDBNavbarItem>

      <MDBNavbarItem class="me-3 me-lg-0 ps-2">
        <MDBBtn outline="light" floating title="Load graph" @click="loadGraph()">
          <MDBIcon icon="book-open"></MDBIcon>
        </MDBBtn>
      </MDBNavbarItem>

      <MDBNavbarItem class="me-3 me-lg-0 ps-2">
        <MDBBtn outline="light" floating title="Save graph" @click="saveGraph()">
          <MDBIcon icon="save"></MDBIcon>
        </MDBBtn>
      </MDBNavbarItem>

      <MDBNavbarItem class="me-3 me-lg-0 ps-4">
        <Field v-model="graphName" label="Graph" class="mb-2" no-separate-label />
      </MDBNavbarItem>

      <MDBNavbarItem class="me-3 me-lg-0 ps-2">
        <MDBBtn outline="light" floating title="Open node/edge detail view window" @click="openDetailWindow()">
          <MDBIcon icon="fas fa-external-link-alt"></MDBIcon>
        </MDBBtn>
      </MDBNavbarItem>

    </MDBNavbarNav>

    <MDBSwitch v-model="linkMode" label="Link mode" />

    <form class="d-flex input-group w-auto ps-4">
      <MDBInput
      class="d-flex w-auto ps-4 border border-end-0"
      inputGroup
      :formOutline="false"
      v-model="input22"
      aria-label="Dollar amount (with dot and two decimal places)"
    >
      <span class="input-group-text border border-start-0" ><MDBIcon icon="search" ></MDBIcon></span>

    </MDBInput>
      <!-- <input
        type="search"
        class="form-control"
        placeholder="Type query"
        aria-label="Search"
      />
      <MDBBtn outline="light"> Search </MDBBtn> -->
    </form>
  </MDBNavbar>

  <ConfigurationPanel />
  <div id="graph-div" ref="graphDiv">
    <v-network-graph ref="graph" class="graph"
    :nodes="nodes" :edges="edges" :layouts="layouts"
    :configs="config" :event-handlers="eventHandlers">

      <template #edge-label="{ edge, ...slotProps }">
        <v-edge-label :text="edge._meta.label" align="center" fill="#ffe7dc" vertical-align="above" v-bind="slotProps" />
      </template>
    </v-network-graph>

  </div>

  <MDBModal
    id="nodeEditor"
    tabindex="-1"
    v-model="displayEditorModal"
    size="lg"
    centered
    scrollable
  >
    <NodeEditor :mode="editorMode" :node-type="currentNodeType" v-model="nodeData"
                @cancel="displayEditorModal=false" @save="nodeEditorUpdated()" />
  </MDBModal>


  <div class="text-center status" :class="{ 'text-danger': hasError }" style="height: 2vh;">
    {{ statusMessage }}
  </div>

</template>

<script setup>

  import axios from "axios";

  import {VNetworkGraph, VEdgeLabel} from "v-network-graph"
  import "v-network-graph/lib/style.css"

  import { useActiveElement, useMagicKeys, whenever } from '@vueuse/core'
  import { logicAnd } from '@vueuse/math'

  import {onMounted, computed, ref} from "vue";
  import { MDBRow, MDBCol, MDBTooltip,
          MDBModal, MDBNavbar, MDBNavbarBrand, MDBNavbarNav, MDBNavbarItem,
          MDBBtn, MDBInput, MDBSwitch, MDBIcon} from "mdb-vue-ui-kit";

  import Field from "./components/Field.vue";
  import NodeEditor from "./components/NodeEditor.vue";
  import ConfigurationPanel from "./components/ConfigurationPanel.vue";

  import { getNodeDisplay } from './graph_nodes_utils.js'

  const statusMessage = ref("Status")
  const hasError = ref(false)

  const displayEditorModal = ref(false)

  const graphName = ref("untitled")
  const graph = ref()
  const graphDiv = ref(null)

  const detailWindow = ref(null)

  const editorMode = ref("")
  const currentNodeType = ref("")

  const newNodePosition = {x: 10, y: 10}

  const nodeData = ref({})
  const linkMode = ref(false)
  const newLinkFrom = ref("")
  const newLinkTo = ref("")

  const activeElement = useActiveElement()

  const notUsingInput = computed(() =>
    activeElement.value?.tagName !== 'INPUT'
    && activeElement.value?.tagName !== 'TEXTAREA',
  )

  const isDetailWindowPresent = () => {
    if (detailWindow.value && detailWindow.value.closed)
      detailWindow.value = null

    return detailWindow.value != null
  }

  const { l } = useMagicKeys()
  whenever(logicAnd(l, notUsingInput), () => {
    if (!displayEditorModal.value) {
      linkMode.value = !linkMode.value
    }

  })

  const nodes = ref({
    // node1: { name: "Node 1" },
    // node2: { name: "Node X" },
    // node3: { name: "Node 3" },
    // node4: { name: "Node 4" },
  })

  const edges = ref({
    // edge1: { source: "node1", target: "node2" },
    // edge2: { source: "node2", target: "node3" },
    // edge3: { source: "node3", target: "node4" },
  })

  const layouts = ref({
    nodes: {
      // node3: { x: 0, y: 0}
    }
  })

  const config = ref({
    view: {
      doubleClickZoomEnabled: false,
      scalingObjects: true,
    },
    node: {
      label: {
        directionAutoAdjustment: true,
        text: node => node._meta.label,
        color: "yellow"
      },
      normal: {
        type: "circle",
        color: (node) => {
          return getNodeDisplay(node)
        }
      }
    },
    edge: {
      marker: {
        target: {
          type: 'arrow'
        }
      }
    }
  })

  const eventHandlers = {
    "node:click":  ({ node }) => {
      // toggle
      if (linkMode.value == false){
        if (isDetailWindowPresent()) {
          let data = nodes.value[node]
          data._key = node
          detailWindow.value.postMessage(
            JSON.stringify({event: 'show-node', data: data}),
            import.meta.env.VITE_WEBSITE_BASE_URL
          )
        }
        return;
      }


      if (newLinkFrom.value == "") {
        newLinkFrom.value = node
      } else if (newLinkTo.value == "") {
        newLinkTo.value = node
        addNewEdge()
      }
    },
    "node:dblclick":  ({ node }) => {
      let data = nodes.value[node]
      data._key = node

      nodeData.value = {...data}
      editorMode.value = 'update'
      currentNodeType.value = 'node'

      displayEditorModal.value = true
    },
    "edge:dblclick": ({ edge }) => {
      let data = edges.value[edge]
      data._key = edge

      nodeData.value = {...data}
      editorMode.value = 'update'
      currentNodeType.value = 'edge'

      displayEditorModal.value = true

    },
    "view:dblclick": async (e) => {

      const viewBox = graph.value.getViewBox()

      editorMode.value = 'new'
      currentNodeType.value = 'node'

      // ** Best so far
      newNodePosition.x = e.event.offsetX + viewBox.left
      newNodePosition.y = e.event.offsetY + viewBox.top

      console.log("new node position", newNodePosition)

      displayEditorModal.value = true
      nodeData.value._key = graphName.value + '-'
      nodeData.value.label = null
      nodeData.value.extraInfo = {}
      nodeData.value._meta = {}
    }
  }

  onMounted(async() => {

  });

  const nodeEditorUpdated = () => {
    if (editorMode.value == 'new' && currentNodeType.value == 'node') {
      addNewNode()
    }

    if (editorMode.value == 'update') {
      updateNode()
    }
  }

  const addNewNode = () => {
    displayEditorModal.value = false

    console.log("New node's data", nodeData.value)

    nodes.value[nodeData.value._key] = JSON.parse(JSON.stringify(nodeData.value))  // deep copy
    layouts.value.nodes[nodeData.value._key] = {x: newNodePosition.x, y: newNodePosition.y}
  }

  const addNewEdge = () => {
    const linkKey = newLinkFrom.value + '_' + newLinkTo.value
    edges.value[linkKey] = { source: newLinkFrom.value, target: newLinkTo.value }
    newLinkFrom.value = ""
    newLinkTo.value = ""
  }

  const updateNode = () => {
    let key = nodeData.value._key
    delete nodeData.value._key

    if (currentNodeType.value == 'node') {
      nodes.value[key] = {...nodeData.value}
    } else {
      edges.value[key] = {...nodeData.value}
    }

    displayEditorModal.value = false
  }

  const newGraph = () => {
    graphName.value = 'New Graph'
    nodes.value = {}
    edges.value = {}
    layouts.value = {nodes: {}}

    statusMessage.value = 'New graph'

  }

  const saveGraph = () => {
    hasError.value = false
    statusMessage.value = 'Sending request'

    let url = import.meta.env.VITE_API_BASE_URL + '/user-graphs';
    console.log(url)

    let postData = {
      graph_name: graphName.value,
      nodes: nodes.value,
      edges: edges.value,
      layouts: layouts.value
    };

    axios.post(url, postData).then(response =>{
      console.log(response)
      statusMessage.value = response.data
      statusMessage.value = '[' + response.status + ' - ' + response.statusText + '] ' +
                            response.data
    }).catch(error =>{
      hasError.value = true
      console.log(error)
      statusMessage.value = '[' + error.response.status + ' - ' + error.response.statusText + '] ' +
                             error.response.data.detail
    })
  }

  const loadGraph = () => {
    hasError.value = false
    statusMessage.value = 'Sending request'

    let url = import.meta.env.VITE_API_BASE_URL + '/user-graphs/' + graphName.value;
    console.log(url)



    axios.get(url).then(response =>{
      console.log(response)
      nodes.value = response.data.nodes
      edges.value = response.data.edges
      layouts.value = response.data.layouts

      statusMessage.value = '[' + response.status + ' - ' + response.statusText + '] Graph loaded'
    }).catch(error =>{
      hasError.value = true
      console.log(error)
      statusMessage.value = '[' + error.response.status + ' - ' + error.response.statusText + '] ' +
                             error.response.data.detail
    })
  }

  const openDetailWindow = () => {
    if (isDetailWindowPresent())
      return

    let url = import.meta.env.VITE_WEBSITE_BASE_URL + '/detail'
    detailWindow.value = window.open(url, "gde_detail")
  }

</script>
