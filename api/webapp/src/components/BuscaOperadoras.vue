<template>
  <div class="busca-operadoras">
    <!-- Barra de pesquisa -->
    <div class="search-bar">
      <input 
        v-model="termoBusca" 
        type="text" 
        placeholder="Digite o nome da operadora..."
        @input="filtrarOperadoras"
      />
      <button @click="buscarOperadoras">Buscar</button>
    </div>

    <!-- Resultados -->
    <div v-if="carregando" class="loading">Carregando...</div>
    
    <div v-else-if="erro" class="error">
      Ocorreu um erro: {{ erro }}
    </div>

    <div v-else>
      <table class="resultados">
        <thead>
          <tr>
          <th>Nome</th>
          <th>Registro ANS</th>
          <th>CNPJ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="operadora in operadorasFiltradas" :key="operadora.registro_ans || operadora.Registro_ANS">
            <td>{{ operadora.nome_fantasia || operadora.Nome_Fantasia || operadora.razao_social || operadora.Razao_Social }}</td>
            <td>{{ operadora.registro_ans || operadora.Registro_ANS }}</td>
            <td>{{ operadora.cnpj || operadora.CNPJ }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BuscaOperadoras',
  data() {
    return {
      termoBusca: '',
      operadoras: [],
      operadorasFiltradas: [],
      carregando: false,
      erro: null
    }
  },
  methods: {
    async buscarOperadoras() {
      this.carregando = true;
      this.erro = null;
      
      try {
        // Constrói a URL com o parâmetro de busca se existir
        let url = 'http://localhost:8000/api/operadoras';
        if (this.termoBusca) {
          url += `?termo=${encodeURIComponent(this.termoBusca)}`;
        }
        
        console.log('Buscando em:', url);
        
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error(`Erro ao buscar operadoras: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Resposta da API:', data.length, 'operadoras encontradas');
        
        if (!Array.isArray(data)) {
          throw new Error('Formato de resposta inválido');
        }
        
        // Atualiza os dados
        this.operadoras = data;
        this.operadorasFiltradas = data;
      } catch (error) {
        console.error('Erro na busca:', error);
        this.erro = error.message;
      } finally {
        this.carregando = false;
      }
    },
    
    // Este método pode ser simplificado já que a filtragem é feita no backend
    filtrarOperadoras() {
      // Agora apenas chama a API novamente com o termo de busca
      this.buscarOperadoras();
    }
  },
  mounted() {
    // Carrega todas operadoras ao iniciar
    this.buscarOperadoras();
  }
}
</script>

<style scoped>
.busca-operadoras {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-bar input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-bar button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.loading, .error {
  padding: 20px;
  text-align: center;
  color: #666;
}

.error {
  color: #ff4444;
}
</style>