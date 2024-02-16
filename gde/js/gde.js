import 'vite/modulepreload-polyfill'

import mountVueComponent from './common_vue.js'

import GDEMain from './GDEMain.vue'
import GDEDetail from './GDEDetail.vue'
import GDETest from './GDETest.vue'

mountVueComponent('gde-main', GDEMain)
mountVueComponent('gde-detail', GDEDetail)
mountVueComponent('gde-test', GDETest)
