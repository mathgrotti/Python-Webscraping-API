<template>
  <div id="app">
    <h1>Consulta de Operadoras ANS</h1>
    <BuscaOperadoras/>
  </div>
</template>

<script>
import BuscaOperadoras from './components/BuscaOperadoras.vue'

export default {
  name: 'App',
  components: {
    BuscaOperadoras
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>