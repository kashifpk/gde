import { createApp } from 'vue'

import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"

function mountVueComponent(elementId, Component, withVNetworkGraph=false) {
    const elem = document.getElementById(elementId)
    const app = createApp(Component)
    if (withVNetworkGraph) {
        app.use(VNetworkGraph)
    }
    app.mount(elem)
}

export default mountVueComponent;
