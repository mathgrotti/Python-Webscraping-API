// /api/webapp/src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',  // Corrigido para usar o proxy
  timeout: 10000
})

export default api