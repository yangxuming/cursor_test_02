import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  const isAuthenticated = computed(() => !!token.value)

  async function register(usernameVal, password) {
    const { data } = await api.post('/register', { username: usernameVal, password })
    token.value = data.access_token
    username.value = data.username
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('username', data.username)
  }

  async function login(usernameVal, password) {
    const { data } = await api.post('/login', { username: usernameVal, password })
    token.value = data.access_token
    username.value = data.username
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('username', data.username)
  }

  function logout() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, isAuthenticated, register, login, logout }
})
