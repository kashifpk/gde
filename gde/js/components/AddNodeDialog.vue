<template>
  <MDBModal
    id="addNodeModel"
    tabindex="-1"
    labelledby="addNodeModelLabel"
    v-model="exampleModal"
  >
    <MDBModalHeader>
      <MDBModalTitle> Add Node </MDBModalTitle>
    </MDBModalHeader>
    <MDBModalBody>
      <MDBInput />
    </MDBModalBody>
    <MDBModalFooter>
      <MDBBtn color="secondary" @click="exampleModal = false">Close</MDBBtn>
      <MDBBtn color="primary">Save changes</MDBBtn>
    </MDBModalFooter>
  </MDBModal>

</template>

<script setup>

import { onMounted, computed, ref, watch} from "vue";
import { MDBModal, MDBModalHeader, MDBModalTitle, MDBModalBody, MDBModalFooter,
         MDBInput, MDBBtn } from "mdb-vue-ui-kit";

const exampleModal = ref(false);
const nodeName = ref("");
const nodeData = ref({
  nodeName: nodeName.value
});


onMounted(async() => {
});


</script>

<style>

</style>

