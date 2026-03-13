<template>
  <div class="chat-layout">
    <Sidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

    <main class="chat-main">
      <template v-if="chatStore.currentConversationId">
        <div class="messages-container" ref="messagesContainer">
          <div class="messages-inner">
            <ChatMessage
              v-for="(msg, idx) in chatStore.messages"
              :key="idx"
              :message="msg"
              :username="authStore.username"
            />
          </div>
        </div>
        <ChatInput :disabled="chatStore.isStreaming" @send="handleSend" />
      </template>

      <div v-else class="empty-chat">
        <div class="empty-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <h2>DeepSeek Chat</h2>
        <p>Start a new conversation to begin chatting with AI</p>
        <button class="start-btn" @click="handleNewChat">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          New Conversation
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import Sidebar from '../components/Sidebar.vue'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'

const authStore = useAuthStore()
const chatStore = useChatStore()
const sidebarCollapsed = ref(false)
const messagesContainer = ref(null)

onMounted(async () => {
  await chatStore.fetchConversations()
  if (chatStore.conversations.length > 0) {
    chatStore.selectConversation(chatStore.conversations[0].id)
  }
})

async function handleSend(content) {
  await chatStore.sendMessage(content)
}

async function handleNewChat() {
  await chatStore.createConversation()
}

watch(
  () => chatStore.messages.length,
  () => {
    nextTick(() => scrollToBottom())
  }
)

watch(
  () => chatStore.messages.at(-1)?.content,
  () => {
    nextTick(() => scrollToBottom())
  }
)

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  background: #0f172a;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 24px;
}

.messages-inner {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 0;
}

.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  gap: 12px;
}

.empty-icon {
  color: #374151;
  margin-bottom: 8px;
}

.empty-chat h2 {
  color: #e5e7eb;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.empty-chat p {
  color: #6b7280;
  font-size: 15px;
  margin: 0;
}

.start-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.start-btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .messages-container {
    padding: 0 12px;
  }
}
</style>
