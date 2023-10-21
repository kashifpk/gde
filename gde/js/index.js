import 'vite/modulepreload-polyfill'

import mountVueComponent from './common_vue.js'

import GDEMain from './GDEMain.vue'

mountVueComponent('vue-section', GDEMain, true);
