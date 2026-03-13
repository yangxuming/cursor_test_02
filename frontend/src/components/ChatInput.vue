<template>
  <div class="chat-input-container">
    <div class="input-wrapper">
      <textarea
        ref="textareaRef"
        v-model="message"
        placeholder="Send a message..."
        rows="1"
        @keydown="handleKeydown"
        @input="autoResize"
        :disabled="disabled"
      ></textarea>
      <button
        class="send-btn"
        @click="send"
        :disabled="!message.trim() || disabled"
        title="Send message"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
        </svg>
      </button>
    </div>
    <p class="hint">Press <kbd>Enter</kbd> to send, <kbd>Shift+Enter</kbd> for new line</p>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

defineProps({ disabled: Boolean })
const emit = defineEmits(['send'])

const message = ref('')
const textareaRef = ref(null)

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

function send() {
  const text = message.value.trim()
  if (!text) return
  emit('send', text)
  message.value = ''
  nextTick(() => autoResize())
}

function autoResize() {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 200) + 'px'
}
</script>

<style scoped>
.chat-input-container {
  padding: 16px 24px 12px;
  border-top: 1px solid #1f2937;
  background: #0f172a;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 12px 16px;
  transition: border-color 0.2s;
}

.input-wrapper:focus-within {
  border-color: #3b82f6;
}

textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: #f1f5f9;
  font-size: 15px;
  line-height: 1.5;
  resize: none;
  outline: none;
  font-family: inherit;
  max-height: 200px;
}

textarea::placeholder {
  color: #475569;
}

textarea:disabled {
  opacity: 0.5;
}

.send-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  min-width: 36px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
}

.send-btn:hover:not(:disabled) {
  opacity: 0.85;
}

.send-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.hint {
  text-align: center;
  color: #4b5563;
  font-size: 12px;
  margin: 8px 0 0;
}

kbd {
  background: #1e293b;
  border: 1px solid #374151;
  border-radius: 3px;
  padding: 1px 5px;
  font-size: 11px;
  font-family: inherit;
}
</style>
