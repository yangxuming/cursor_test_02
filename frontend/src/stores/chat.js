import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversationId = ref(null)
  const messages = ref([])
  const isStreaming = ref(false)

  async function fetchConversations() {
    const { data } = await api.get('/conversations')
    conversations.value = data
  }

  async function createConversation(title = 'New Conversation') {
    const { data } = await api.post('/conversations', { title })
    conversations.value.unshift(data)
    currentConversationId.value = data.id
    messages.value = []
    return data
  }

  async function deleteConversation(id) {
    await api.delete(`/conversations/${id}`)
    conversations.value = conversations.value.filter((c) => c.id !== id)
    if (currentConversationId.value === id) {
      currentConversationId.value = conversations.value[0]?.id || null
      messages.value = []
    }
  }

  async function renameConversation(id, title) {
    const { data } = await api.put(`/conversations/${id}`, { title })
    const conv = conversations.value.find((c) => c.id === id)
    if (conv) conv.title = data.title
  }

  function selectConversation(id) {
    currentConversationId.value = id
    messages.value = []
  }

  async function sendMessage(content) {
    if (!currentConversationId.value || isStreaming.value) return

    messages.value.push({ role: 'user', content })

    const assistantMsg = { role: 'assistant', content: '' }
    messages.value.push(assistantMsg)

    isStreaming.value = true

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: content,
          conversation_id: currentConversationId.value,
        }),
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data:')) {
            const dataStr = line.slice(5).trim()
            if (!dataStr) continue
            try {
              const data = JSON.parse(dataStr)
              if (data.content) {
                assistantMsg.content += data.content
              }
              if (data.error) {
                assistantMsg.content += `\n\nError: ${data.error}`
              }
            } catch {
              // ignore non-JSON lines
            }
          }
        }
      }
    } catch (error) {
      assistantMsg.content += `\n\nConnection error: ${error.message}`
    } finally {
      isStreaming.value = false
    }
  }

  return {
    conversations,
    currentConversationId,
    messages,
    isStreaming,
    fetchConversations,
    createConversation,
    deleteConversation,
    renameConversation,
    selectConversation,
    sendMessage,
  }
})
