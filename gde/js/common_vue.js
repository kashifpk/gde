import { createApp } from 'vue'


function mountVueComponent(elementId, Component) {
  const elem = document.getElementById(elementId)
  const app = createApp(Component)
  // Register a global custom directive called `v-focus`
  // app.directive('focus', {
  //   // When the bound element is mounted into the DOM...
  //   mounted(el) {
  //   // Focus the element
  //   el.focus()
  //   }
  // })
  app.mount(elem)
}

export default mountVueComponent;
