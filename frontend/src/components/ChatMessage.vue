<template>
  <div class="message" :class="message.role">
    <div class="message-avatar">
      <div v-if="message.role === 'user'" class="avatar user-avatar">
        {{ initial }}
      </div>
      <div v-else class="avatar ai-avatar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7l10 5 10-5-10-5z" /><path d="M2 17l10 5 10-5" /><path d="M2 12l10 5 10-5" />
        </svg>
      </div>
    </div>
    <div class="message-body">
      <div class="message-role">{{ message.role === 'user' ? 'You' : 'DeepSeek' }}</div>
      <div class="message-content" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'

const props = defineProps({
  message: { type: Object, required: true },
  username: { type: String, default: '' },
})

const initial = computed(() =>
  props.username ? props.username.charAt(0).toUpperCase() : 'U'
)

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    const escapedStr = md.utils.escapeHtml(str)
    const langLabel = lang || 'code'
    if (lang && hljs.getLanguage(lang)) {
      try {
        const highlighted = hljs.highlight(str, { language: lang, ignoreIllegals: true }).value
        return `<div class="code-block"><div class="code-header"><span class="code-lang">${langLabel}</span><button class="copy-btn" onclick="navigator.clipboard.writeText(decodeURIComponent('${encodeURIComponent(str)}'))">Copy</button></div><pre><code class="hljs language-${lang}">${highlighted}</code></pre></div>`
      } catch {
        // fall through
      }
    }
    return `<div class="code-block"><div class="code-header"><span class="code-lang">${langLabel}</span><button class="copy-btn" onclick="navigator.clipboard.writeText(decodeURIComponent('${encodeURIComponent(str)}'))">Copy</button></div><pre><code class="hljs">${escapedStr}</code></pre></div>`
  },
})

const renderedContent = computed(() => {
  if (!props.message.content) return '<span class="typing-cursor"></span>'
  return md.render(props.message.content)
})
</script>

<style scoped>
.message {
  display: flex;
  gap: 16px;
  padding: 24px 0;
}

.message + .message {
  border-top: 1px solid #1f2937;
}

.message.assistant {
  background: rgba(31, 41, 55, 0.3);
  margin: 0 -24px;
  padding: 24px;
  border-radius: 8px;
}

.avatar {
  width: 32px;
  height: 32px;
  min-width: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

.user-avatar {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
}

.ai-avatar {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.message-body {
  flex: 1;
  min-width: 0;
}

.message-role {
  font-size: 13px;
  font-weight: 600;
  color: #d1d5db;
  margin-bottom: 6px;
}

.message-content {
  color: #e5e7eb;
  font-size: 15px;
  line-height: 1.7;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.message-content :deep(p) {
  margin: 0 0 12px;
}

.message-content :deep(p:last-child) {
  margin-bottom: 0;
}

.message-content :deep(ul),
.message-content :deep(ol) {
  margin: 0 0 12px;
  padding-left: 24px;
}

.message-content :deep(.code-block) {
  margin: 12px 0;
  border-radius: 8px;
  overflow: hidden;
  background: #0d1117;
  border: 1px solid #21262d;
}

.message-content :deep(.code-header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #161b22;
  border-bottom: 1px solid #21262d;
}

.message-content :deep(.code-lang) {
  font-size: 12px;
  color: #8b949e;
  font-weight: 500;
}

.message-content :deep(.copy-btn) {
  padding: 4px 10px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 4px;
  color: #8b949e;
  font-size: 12px;
  cursor: pointer;
  transition: color 0.15s;
}

.message-content :deep(.copy-btn:hover) {
  color: #e6edf3;
}

.message-content :deep(pre) {
  margin: 0;
  padding: 16px;
  overflow-x: auto;
}

.message-content :deep(code) {
  font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.5;
}

.message-content :deep(:not(pre) > code) {
  background: #1f2937;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  color: #f0abfc;
}

.message-content :deep(blockquote) {
  border-left: 3px solid #3b82f6;
  margin: 12px 0;
  padding: 4px 16px;
  color: #9ca3af;
}

.message-content :deep(table) {
  border-collapse: collapse;
  margin: 12px 0;
  width: 100%;
}

.message-content :deep(th),
.message-content :deep(td) {
  border: 1px solid #374151;
  padding: 8px 12px;
  text-align: left;
}

.message-content :deep(th) {
  background: #1f2937;
  font-weight: 600;
}

.message-content :deep(a) {
  color: #60a5fa;
  text-decoration: none;
}

.message-content :deep(a:hover) {
  text-decoration: underline;
}

:deep(.typing-cursor) {
  display: inline-block;
  width: 8px;
  height: 18px;
  background: #60a5fa;
  animation: blink 1s step-end infinite;
  vertical-align: text-bottom;
  border-radius: 1px;
}

@keyframes blink {
  50% { opacity: 0; }
}
</style>
