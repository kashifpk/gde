import 'vite/modulepreload-polyfill'

import mountVueComponent from './common_vue.js'

import VueHello from './VueHello.vue'

mountVueComponent('vue-section', VueHello, true);
