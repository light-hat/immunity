<template>
  <div style="height: 100vh">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        fit-view-on-init
        class="vue-flow-basic-example"
        :default-zoom="1.5"
        :min-zoom="0.2"
        :max-zoom="4"
      >
        <Background pattern-color="#aaa" :gap="8" />

        <MiniMap />

        <Controls />

        <template #node-custom="nodeProps">
          <CustomNode v-bind="nodeProps" />
        </template>

        <template #edge-custom="edgeProps">
          <CustomEdge v-bind="edgeProps" />
        </template>
      </VueFlow>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import axios from '../axios'
import { VueFlow } from '@vue-flow/core'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'

import SpecialNode from '../components/SpecialNode.vue'
import SpecialEdge from '../components/SpecialEdge.vue'

export default {
  components: { VueFlow },
  setup() {
    const auth = useAuthStore()
    const router = useRouter()

    const nodes = ref([])
    const edges = ref([])

    onMounted(async () => {
      try {
        const response = await axios.get('graph/data', {
          headers: {
            Authorization: `Bearer ${auth.accessToken}`
          }
        })
        nodes.value = response.data.nodes
        edges.value = response.data.edges
      } catch (error) {
        console.error('Error fetching graph data', error)
        // Можно при ошибке перенаправить на login, если 401
        // или показать уведомление.
      }
    })

    return { nodes, edges }
  }
}
</script>

<style>
/* these are necessary styles for vue flow */
@import '@vue-flow/core/dist/style.css';

/* this contains the default theme, these are optional styles */
@import '@vue-flow/core/dist/theme-default.css';
</style>
