// Single place that knows about the backend. Every page imports from
// here instead of calling axios directly, so the base URL or the
// response envelope only needs to change in one spot.
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

export const studentApi = {
  list: (params) => client.get('/students/', { params }),
  get: (id) => client.get(`/students/${id}/`),
  create: (payload) => client.post('/students/', payload),
  update: (id, payload) => client.put(`/students/${id}/`, payload),
  remove: (id) => client.delete(`/students/${id}/`),
}

export default client
