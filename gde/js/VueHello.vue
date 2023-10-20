<template>
    Hello {{ name }}!!!

    <v-network-graph class="graph" :nodes="nodes" :edges="edges" />
</template>

<script setup>

import {getCurrentInstance, onMounted, computed, ref, watch} from "vue";

const name = ref("VueJS");

const nodes = {
  node1: { name: "Node 1" },
  node2: { name: "Node X" },
  node3: { name: "Node 3" },
  node4: { name: "Node 4" },
}

const edges = {
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
}

onMounted(async() => {
});


</script>

<style>
.graph {
  width: 800px;
  height: 600px;
  border: 1px solid #000;
}
</style>

