<template>
  <div class="container">
    <h1>Consulta de Operadoras ANS</h1>
    
    <div class="search-box">
      <input
        v-model="termoBusca"
        @keyup.enter="buscarOperadoras"
        placeholder="Digite nome, registro ANS ou CNPJ..."
        class="search-input"
      />
      <button @click="buscarOperadoras" :disabled="!termoBusca.trim()">
        Buscar
      </button>
    </div>

    <!-- Estados da busca -->
    <div v-if="carregando" class="status-message">Carregando...</div>
    <div v-else-if="erro" class="error-message">{{ erro }}</div>
    <div v-else-if="termoBusca && operadoras.length === 0" class="status-message">
      Nenhum resultado encontrado para "{{ termoBusca }}"
    </div>

    <!-- Resultados -->
    <div v-if="operadoras.length > 0" class="results-container">
      <div class="results-header">
        <h2>Resultados para "{{ termoBusca }}" ({{ operadoras.length }})</h2>
      </div>
      
      <div class="operadora-card" v-for="op in operadoras" :key="op.Registro_ANS">
        <h3>{{ op.Nome_Fantasia || op.Razao_Social }}</h3>
        <div class="operadora-info">
          <p><strong>Registro ANS:</strong> {{ op.Registro_ANS }}</p>
          <p><strong>CNPJ:</strong> {{ formatCNPJ(op.CNPJ) }}</p>
          <p><strong>Modalidade:</strong> {{ op.Modalidade }}</p>
          <p><strong>Cidade/UF:</strong> {{ op.Cidade }}/{{ op.UF }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const termoBusca = ref('');
const operadoras = ref([]);
const carregando = ref(false);
const erro = ref(null);

const formatCNPJ = (cnpj) => {
  if (!cnpj) return 'Não informado';
  // Formatação: 00.000.000/0000-00
  return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};

const buscarOperadoras = async () => {
  if (!termoBusca.value.trim()) return;

  try {
    carregando.value = true;
    erro.value = null;
    operadoras.value = [];
    
    const response = await axios.get('/api/operadoras', {
      params: { 
        termo: termoBusca.value.trim().toLowerCase() 
      }
    });
    
    // Filtra resultados vazios e remove possíveis caracteres especiais
    operadoras.value = response.data.operadoras
      .filter(op => op.Nome_Fantasia || op.Razao_Social)
      .map(op => ({
        ...op,
        Nome_Fantasia: op.Nome_Fantasia?.trim(),
        Razao_Social: op.Razao_Social?.trim()
      }));
      
  } catch (err) {
    erro.value = 'Erro ao buscar operadoras.';
    console.error('Erro:', err.response?.data || err.message);
  } finally {
    carregando.value = false;
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.status-message, .error-message {
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
  text-align: center;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
}

.status-message {
  background-color: #e3f2fd;
  color: #1976d2;
}

.results-container {
  margin-top: 20px;
}

.results-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.operadora-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.operadora-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.operadora-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.operadora-info p {
  margin: 5px 0;
}
</style>