<template>
  <aside class="sidebar" :class="{ collapsed: collapsed }">
    <div class="sidebar-header">
      <button class="new-chat-btn" @click="handleNewChat">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        <span v-if="!collapsed">New Chat</span>
      </button>
      <button class="toggle-btn" @click="$emit('toggle')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>
    </div>

    <div class="conversation-list" v-if="!collapsed">
      <div
        v-for="conv in chatStore.conversations"
        :key="conv.id"
        class="conversation-item"
        :class="{ active: conv.id === chatStore.currentConversationId }"
        @click="chatStore.selectConversation(conv.id)"
      >
        <template v-if="editingId === conv.id">
          <input
            v-model="editTitle"
            class="edit-input"
            @keyup.enter="saveRename(conv.id)"
            @keyup.escape="cancelRename"
            @blur="saveRename(conv.id)"
            ref="editInput"
          />
        </template>
        <template v-else>
          <span class="conv-title">{{ conv.title }}</span>
          <div class="conv-actions" @click.stop>
            <button class="action-btn" @click="startRename(conv)" title="Rename">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
              </svg>
            </button>
            <button class="action-btn delete" @click="handleDelete(conv.id)" title="Delete">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
            </button>
          </div>
        </template>
      </div>
      <div v-if="chatStore.conversations.length === 0" class="empty-state">
        No conversations yet
      </div>
    </div>

    <div class="sidebar-footer" v-if="!collapsed">
      <div class="user-info">
        <div class="avatar">{{ authStore.username.charAt(0).toUpperCase() }}</div>
        <span class="username">{{ authStore.username }}</span>
      </div>
      <button class="logout-btn" @click="handleLogout" title="Logout">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" />
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'

defineProps({ collapsed: Boolean })
defineEmits(['toggle'])

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const editingId = ref(null)
const editTitle = ref('')
const editInput = ref(null)

async function handleNewChat() {
  await chatStore.createConversation()
}

function startRename(conv) {
  editingId.value = conv.id
  editTitle.value = conv.title
  nextTick(() => {
    if (editInput.value) {
      const el = Array.isArray(editInput.value) ? editInput.value[0] : editInput.value
      el?.focus()
    }
  })
}

async function saveRename(id) {
  if (editTitle.value.trim() && editTitle.value !== '') {
    await chatStore.renameConversation(id, editTitle.value.trim())
  }
  editingId.value = null
}

function cancelRename() {
  editingId.value = null
}

async function handleDelete(id) {
  await chatStore.deleteConversation(id)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  min-width: 280px;
  background: #111827;
  border-right: 1px solid #1f2937;
  display: flex;
  flex-direction: column;
  height: 100vh;
  transition: width 0.2s, min-width 0.2s;
}

.sidebar.collapsed {
  width: 60px;
  min-width: 60px;
}

.sidebar-header {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-bottom: 1px solid #1f2937;
}

.new-chat-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 8px;
  color: #e5e7eb;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}

.new-chat-btn:hover {
  background: #374151;
}

.collapsed .new-chat-btn {
  padding: 10px 0;
}

.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  background: transparent;
  border: 1px solid #374151;
  border-radius: 8px;
  color: #9ca3af;
  cursor: pointer;
  transition: color 0.2s;
}

.toggle-btn:hover {
  color: #e5e7eb;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  margin-bottom: 2px;
}

.conversation-item:hover {
  background: #1f2937;
}

.conversation-item.active {
  background: #1f2937;
}

.conv-title {
  flex: 1;
  color: #d1d5db;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-actions {
  display: none;
  gap: 4px;
}

.conversation-item:hover .conv-actions {
  display: flex;
}

.action-btn {
  padding: 4px;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.action-btn:hover {
  color: #d1d5db;
  background: #374151;
}

.action-btn.delete:hover {
  color: #f87171;
}

.edit-input {
  flex: 1;
  background: #0f172a;
  border: 1px solid #3b82f6;
  border-radius: 4px;
  color: #f1f5f9;
  padding: 4px 8px;
  font-size: 13px;
  outline: none;
}

.empty-state {
  text-align: center;
  color: #4b5563;
  font-size: 13px;
  padding: 40px 20px;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid #1f2937;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.username {
  color: #d1d5db;
  font-size: 13px;
  font-weight: 500;
}

.logout-btn {
  padding: 8px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.logout-btn:hover {
  color: #f87171;
  background: rgba(248, 113, 113, 0.1);
}
</style>
