<style>
.linked-content {
  display: flex;
  gap: 1em;
  margin-left: 1em;
}
</style>

<template>

  <h2>GDE Detail {{ itemData._key }}</h2>
  <NodeInfoDisplay v-if="Object.keys(itemData).length > 0" :node-info="itemData" show-links />

  <code>{{ JSON.stringify(itemData, null, 2) }}</code>
</template>

<script setup>
  import {onMounted, ref} from "vue";
  import { MDBTable, MDBRow, MDBCol } from "mdb-vue-ui-kit";
  import axios from "axios";
  import NodeInfoDisplay from "./components/NodeInfoDisplay.vue";


  const event = ref("")
  const itemKey = ref("")  // tmp1-bajwa
  const itemData = ref({})
  const firstLevelKeys = ref([])
  const hiddenFields = ref(['extra_info', '_meta', '_key', '_links'])
  onMounted(async () => {
    itemKey.value = window.ITEM_KEY
    console.log("itemKey", itemKey.value)
    if (itemKey.value == "") {
      // opened from main window so setup inter-window communication
      window.addEventListener("message", showDetail, false)
    } else {
      // opened directly so fetch item data via API
      let url = import.meta.env.VITE_API_BASE_URL + '/items/' + itemKey.value;

      // get data from url and set it as itemData using async-await syntax
      const response = await axios.get(url);
      itemData.value = response.data;
      processItemData()
    }

  });

  const processItemData = () => {
    // get all property names from itemData.value into firstLevelKeys array
    firstLevelKeys.value = Object.keys(itemData.value)

    // remove hiddenFields values from firstLevelKeys
    firstLevelKeys.value = firstLevelKeys.value.filter(k => !hiddenFields.value.includes(k))
  }

  const showDetail = (event) => {

    console.log("request received to show detial")
    console.log(event)
    try {
      let eData = JSON.parse(event.data)
      event.value = eData.event
      itemData.value = eData.data

      processItemData()

      // event.source.console.log('hey detailer')
    } catch (e) {

    }

  }

</script>
