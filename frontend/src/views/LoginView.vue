<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <h1>DeepSeek Chat</h1>
        <p class="subtitle">AI-powered conversation assistant</p>
      </div>

      <div class="tab-switch">
        <button :class="{ active: !isRegister }" @click="isRegister = false">Sign In</button>
        <button :class="{ active: isRegister }" @click="isRegister = true">Sign Up</button>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Enter your username"
            required
            minlength="2"
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            required
            minlength="6"
            autocomplete="current-password"
          />
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <button type="submit" class="submit-btn" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Please wait...' : isRegister ? 'Create Account' : 'Sign In' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isRegister = ref(false)
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    if (isRegister.value) {
      await authStore.register(username.value, password.value)
    } else {
      await authStore.login(username.value, password.value)
    }
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 20px;
}

.login-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 14px;
  color: white;
  margin-bottom: 16px;
}

.login-header h1 {
  color: #f1f5f9;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
}

.subtitle {
  color: #94a3b8;
  font-size: 14px;
  margin: 0;
}

.tab-switch {
  display: flex;
  background: #0f172a;
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 28px;
}

.tab-switch button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-switch button.active {
  background: #334155;
  color: #f1f5f9;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: #cbd5e1;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 10px;
  color: #f1f5f9;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #3b82f6;
}

.form-group input::placeholder {
  color: #475569;
}

.error-message {
  color: #f87171;
  font-size: 13px;
  margin: 0 0 16px;
  padding: 10px 14px;
  background: rgba(248, 113, 113, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(248, 113, 113, 0.2);
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
