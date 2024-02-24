<style scoped>

  .node-container {
    border-left: solid 3px #fff;
    padding-left: 1em;
  }

  .node-info {
    /* padding: 1em; */
    display: flex;
    gap: 2em;
    padding-bottom: 2em;

  }
</style>

<template>
  <div class="node-container" :style="{ borderColor: getRandomColor() }">
    <h5 v-if="title"> {{ title }}</h5>
    <h4>{{nodeInfo._meta.label}}</h4>
    <div class="node-info">

      <img
        v-if="nodeInfo._meta.display_type=='image'"
        :src="nodeInfo._meta.display_value" style="max-width: 100%;"
      />
      <MDBTable responsive striped hover dark>
        <tbody>
          <tr v-for="k in firstLevelKeys">
            <th style="width: 15%;">{{ k }}</th>
            <td>{{ nodeInfo[k] }}</td>
          </tr>
        </tbody>
      </MDBTable>

      <hr />
      <MDBTable responsive striped hover dark v-if="nodeInfo.hasOwnProperty('extra_info')">
        <tbody>
          <tr v-for="k in Object.keys(nodeInfo.extra_info)">
            <th style="width: 15%;">{{ k }}</th>
            <td>{{ nodeInfo.extra_info[k] }}</td>
          </tr>
        </tbody>
      </MDBTable>
    </div>

    <div v-if="showLinks==true && nodeInfo._links.length > 0" class="linked-content">
      <div v-for="linkData in nodeInfo._links">
        <NodeInfoDisplay :title="linkTitle(linkData)" :node-info="linkData.linked_node" />
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
  import { onMounted, ref } from "vue"
  import { MDBTable } from "mdb-vue-ui-kit";
  import type {LinkInfo, NodeInformationSchema} from "../type_defs.ts"

  interface Props {
    title: String | unknown
    showLinks?: boolean
    nodeInfo: NodeInformationSchema
  }
  const props = defineProps<Props>()

  const firstLevelKeys = ref([])
  const hiddenFields = ref(['extra_info', '_meta', '_key', '_links'])
  onMounted(async () => {
    // get all property names from itemData.value into firstLevelKeys array
    firstLevelKeys.value = Object.keys(props.nodeInfo)

    // remove hiddenFields values from firstLevelKeys
    firstLevelKeys.value = firstLevelKeys.value.filter(k => !hiddenFields.value.includes(k))

  })

  const getRandomColor = () => {
    return "hsl(" + Math.random() * 360 + ", 100%, 75%)";
  }

  const linkTitle = (link: LinkInfo) => {
    console.log('----------------')
    console.log(props.nodeInfo)
    console.log(link)
    if (link.source == props.nodeInfo._key)
      return props.nodeInfo._meta.label + " -> " + link._meta.label + " -> " + link.linked_node._meta.label
    else
      return link.linked_node._meta.label +  " -> " + link._meta.label + " -> " + props.nodeInfo._meta.label
  }

</script>