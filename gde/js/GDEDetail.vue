<style>


</style>

<template>

  <h2>GDE Detail</h2>
  <code>{{ JSON.stringify(eventData, null, 2) }}</code>
  <MDBTable responsive striped hover dark border="dark">
    <tbody>
      <tr v-for="k in Object.keys(eventData)">
        <th style="width: 15%;">{{ k }}</th>
        <td>{{ eventData[k] }}</td>
      </tr>
    </tbody>
  </MDBTable>
</template>

<script setup>
  import {onMounted, ref} from "vue";
  import { MDBTable } from "mdb-vue-ui-kit";

  const event = ref("")
  const eventData = ref("")
  onMounted(() => {
    window.addEventListener("message", showDetail, false)
  });

  const showDetail = (event) => {

    console.log("request received to show detial")
    console.log(event)
    try {
      let eData = JSON.parse(event.data)
      event.value = eData.event
      eventData.value = eData.data
      // event.source.console.log('hey detailer')
    } catch (e) {

    }

  }

</script>
