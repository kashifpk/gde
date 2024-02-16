<style>


</style>

<template>

  <h2>GDE Test</h2>
  <i class="fas fa-user"></i>
  <v-network-graph
    :nodes="nodes"
    :edges="edges"
    :layouts="layouts"
    :configs="configs"
  >
    <!-- Use CSS to define references to external fonts.
         To use CSS within SVG, use <defs>. -->
    <defs>
      <!-- Cannot use <style> directly due to restrictions of Vue. -->
      <component is="style">
        @font-face { font-family: 'Material Icons'; font-style: normal; font-weight:
        400; src:
        url(https://fonts.gstatic.com/s/materialicons/v97/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.woff2)
        format('woff2'); }
      </component>
    </defs>

    <!-- Replace the node component -->
    <template #override-node="{ nodeId, scale, config, ...slotProps }">
      <circle :r="config.radius * scale" :fill="config.color" v-bind="slotProps" />
      <!-- Use v-html to interpret escape sequences for icon characters. -->
      <text
        font-family="Material Icons"
        :font-size="22 * scale"
        fill="#ffffff"
        text-anchor="middle"
        dominant-baseline="central"
        style="pointer-events: none"
        v-html="nodes[nodeId].icon"
      />
    </template>

  </v-network-graph>

</template>

<script setup>
  import {onMounted, ref} from "vue";
  import { defineConfigs, VNetworkGraph, VEdgeLabel } from "v-network-graph"
  import "v-network-graph/lib/style.css"

  const edges = {
    edge1: { source: "node1", target: "node2" },
    edge2: { source: "node2", target: "node3" },
    edge3: { source: "node2", target: "node4" },
    edge4: { source: "node4", target: "node5" },
    edge5: { source: "node4", target: "node6" },
  }

  const layouts = {
    nodes: {
      node1: { x: 0, y: 0 },
      node2: { x: 80, y: 80 },
      node3: { x: 0, y: 160 },
      node4: { x: 240, y: 80 },
      node5: { x: 320, y: 0 },
      node6: { x: 320, y: 160 },
    },
  }

  const configs = defineConfigs({
    node: {
      selectable: true,
      normal: {
        radius: 20,
      },
      hover: {
        radius: 22,
      },
    },
  })

  const nodes = {
    node1: { name: "N1", icon: "&#xe320" /* Laptop Mac */ },
    node2: { name: "N2", icon: "&#xe328" /* Router */ },
    node3: { name: "N3", icon: "&#xe331" /* Tablet Mac */ },
    node4: { name: "N4", icon: "&#xe2bd" /* Cloud */ },
    node5: { name: "N5", icon: "&#xf0e2" /* Support Agent */ },
    node6: { name: "N6", icon: "&#xea75" /* Video Settings */ },
  }
</script>
