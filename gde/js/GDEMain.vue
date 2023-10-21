<template>
  <MDBRow><MDBCol>Hello {{ name }}!!! </MDBCol></MDBRow>
  <MDBRow>
    <MDBCol col="2"><MDBBtn>Add node</MDBBtn></MDBCol>
    <MDBCol>
      <div ref="graphDiv">
        <v-network-graph ref="graph" class="graph"
        :nodes="nodes" :edges="edges" :layouts="layouts"
        :configs="config" :event-handlers="eventHandlers" />
      </div>

    </MDBCol>
  </MDBRow>
  <MDBModal
    id="addNodeModel"
    tabindex="-1"
    labelledby="addNodeModelLabel"
    v-model="displayAddNodeDialog"
    centered
  >
    <MDBModalHeader>
      <MDBModalTitle> Add Node </MDBModalTitle>
    </MDBModalHeader>
    <MDBModalBody>
      <MDBInput ref="nodeNameTextBox" label="Node name" v-model="newNodeName" />
    </MDBModalBody>
    <MDBModalFooter>
      <MDBBtn color="secondary" @click="displayAddNodeDialog = false">Close</MDBBtn>
      <MDBBtn color="primary" @click="addNewNode()">Save changes</MDBBtn>
    </MDBModalFooter>
  </MDBModal>

</template>

<script setup>

import {getCurrentInstance, onMounted, computed, ref, watch} from "vue";
import { MDBRow, MDBCol,
         MDBModal, MDBModalHeader, MDBModalTitle, MDBModalBody, MDBModalFooter,
         MDBBtn, MDBInput, } from "mdb-vue-ui-kit";

const name = ref("VueJS")
const graph = ref()
const graphDiv = ref(null)
const nodeNameTextBox = ref()
const displayAddNodeDialog = ref(false)
const newNodeName = ref("")
const newNodePosition = {x: 10, y: 10}


const nodes = ref({
  node1: { name: "Node 1" },
  node2: { name: "Node X" },
  node3: { name: "Node 3" },
  node4: { name: "Node 4" },
})

const edges = ref({
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
})

const layouts = ref({
  nodes: {
    node3: { x: 0, y: 0}
  }
})

const config = ref({
  view: {
    doubleClickZoomEnabled: false,
    scalingObjects: true,
  }
})



const eventHandlers = {
  "view:dblclick": (e) => {
    console.log(e)
    console.log("Event x and y", e.event.x, e.event.y)
    console.log("Event offset x and y", e.event.offsetX, e.event.offsetY)
    console.log("Event client x and y", e.event.clientX, e.event.clientY)

    const viewBox = graph.value.getViewBox()
    const svgSize = graph.value.getSizes()
    const domPos = graph.value.translateFromSvgToDomCoordinates({x: e.event.x, y: e.event.y})
    const svgPos = graph.value.translateFromDomToSvgCoordinates({x: e.event.x, y: e.event.y})
    console.log("viewBox", viewBox)
    console.log("domPos", domPos)
    console.log("svgPos", svgPos)
    // ** Best so far
    // newNodePosition.x = e.event.offsetX - (domPos.x / 2)
    // newNodePosition.y = e.event.offsetY - (domPos.y / 2)
    newNodePosition.x = e.event.offsetX + viewBox.left
    newNodePosition.y = e.event.offsetY + viewBox.top

    // newNodePosition.x = e.event.x - (svgSize.width / 2)
    // newNodePosition.y = e.event.y - (svgSize.height / 2)

    // newNodePosition.x = e.event.offsetX - (graphDiv.value.clientWidth / 2)
    // newNodePosition.y = e.event.offsetY - (graphDiv.value.clientHeight / 2)
    console.log("new node position", newNodePosition)
    // newNodePosition.x = e.event.offsetX
    // newNodePosition.y = e.event.offsetY
    displayAddNodeDialog.value = true
    // console.log(nodeNameTextBox)
    // nodeNameTextBox.value.focus()
  }
}

onMounted(async() => {
  console.log(graph.value)
  console.log(graphDiv.value)
});

const addNewNode = () => {
  displayAddNodeDialog.value = false;
  nodes.value[newNodeName.value] = { name: newNodeName.value}
  layouts.value.nodes[newNodeName.value] = {x: newNodePosition.x, y: newNodePosition.y}
}

</script>

<style>
.graph {
  border: 1px solid #c0c0c0;
  height: 80vh;

}
</style>

