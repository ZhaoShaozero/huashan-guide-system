<template>
  <div class="chat-page">
    <h2>🤖 AI 智能华山导游</h2>
    <p class="subtitle">
      可以问：怎么登华山？长空栈道危不危险？哪条路线适合我？一日游怎么安排？
    </p>

    <div class="chat-window card">
      <div v-if="messages.length === 0" class="empty-tips">
        <p>👋 你好！我是华山智能导游</p>
        <p>可以帮助你：</p>
        <ul>
          <li>规划登山路线</li>
          <li>解释各个景点的特点和风险</li>
          <li>给出不同人群的游玩建议</li>
        </ul>
      </div>

      <div v-for="m in messages" :key="m.id" :class="['msg', m.type]">
        <div class="bubble">
          {{ m.content }}
        </div>
      </div>

      <!-- 加载动画 -->
      <div v-if="isLoading" class="msg bot">
        <div class="bubble loading">
          <span></span><span></span><span></span>
        </div>
      </div>

      <div ref="messagesEnd"></div>
    </div>

    <!-- 输入区 -->
    <div class="input-row">
      <input
        v-model="q"
        class="input-field"
        placeholder="请输入你的问题，按 Enter 发送…"
        @keyup.enter="send"
        :disabled="isLoading"
      />
      <button
        class="send-btn"
        @click="send"
        :disabled="isLoading || !q.trim()"
      >
        {{ isLoading ? '…' : '发送' }}
      </button>
    </div>

    <!-- 快捷提问 -->
    <div class="quick card">
      <span class="label">💡 快捷提问：</span>
      <div class="quick-buttons">
        <button
          v-for="item in quickQuestions"
          :key="item"
          @click="quickAsk(item)"
          :disabled="isLoading"
          class="quick-btn"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <div class="card tips">
      <p>
        💾 <strong>提示：</strong>刷新页面后对话记录会清除。
        <button @click="clearHistory" class="clear-btn">清空历史</button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'

// const API_BASE = 'http://127.0.0.1:15500'
// const API_BASE = ''
const API_BASE = 'https://trip.zhsu.online/' 

const messages = ref([
  {
    id: 1,
    type: 'bot',
    content:
      '你好，我是华山智能导游，可以帮你规划路线、说明风险点、解答游玩问题。请告诉我你的情况，例如“体力一般，想一日游”，我会给你建议。',
  },
])
const q = ref('')
const isLoading = ref(false)
const messagesEnd = ref(null)
let mid = 2

const quickQuestions = [
  '怎么登华山比较合适？',
  '长空栈道危不危险？',
  '体力一般适合走哪条路线？',
  '想看日出应该怎么安排？',
  '华山一日游如何规划？',
  '有恐高应该避开什么路段？',
]

const scrollToBottom = () => {
  nextTick(() => {
    messagesEnd.value?.scrollIntoView({ behavior: 'smooth' })
  })
}

const send = async () => {
  if (!q.value.trim() || isLoading.value) return

  const question = q.value.trim()
  messages.value.push({ id: mid++, type: 'user', content: question })
  q.value = ''
  scrollToBottom()

  isLoading.value = true

  try {
    const res = await axios.post(
      `${API_BASE}/api/ai/ask`,
      { question },
      { timeout: 30000 },
    )
    messages.value.push({
      id: mid++,
      type: 'bot',
      content: res.data.answer || '暂时无法获取回答，请稍后重试。',
    })
  } catch (e) {
    console.error('AI 请求错误：', e)
    let msg = '暂时无法连接到 AI 服务，请稍后再试。'
    if (!navigator.onLine) {
      msg = '网络连接已断开，请检查网络。'
    }
    messages.value.push({
      id: mid++,
      type: 'bot',
      content: msg,
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const quickAsk = (text) => {
  if (isLoading.value) return
  q.value = text
  nextTick(() => send())
}

const clearHistory = () => {
  if (confirm('确认要清空所有对话记录吗？')) {
    messages.value = [
      {
        id: 1,
        type: 'bot',
        content:
          '你好，我是华山智能导游，可以帮你规划路线、说明风险点、解答游玩问题。请告诉我你的情况，例如“体力一般，想一日游”，我会给你建议。',
      },
    ]
    mid = 2
    q.value = ''
    scrollToBottom()
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.subtitle {
  font-size: 14px;
  color: #555;
  margin-bottom: 4px;
}

.card {
  background: #fff;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* 聊天窗口 */
.chat-window {
  min-height: 300px;
  max-height: 480px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: linear-gradient(180deg, #fafafa 0%, #fff 100%);
}

.empty-tips {
  text-align: center;
  color: #999;
  font-size: 14px;
  line-height: 1.6;
}
.empty-tips p:first-child {
  font-size: 16px;
  color: #333;
}
.empty-tips ul {
  list-style: none;
  padding: 0;
  margin-top: 8px;
}
.empty-tips li {
  padding: 3px 0;
}
.empty-tips li::before {
  content: '✓ ';
  color: #667eea;
}

.msg {
  display: flex;
}
.msg.user {
  justify-content: flex-end;
}
.msg.bot {
  justify-content: flex-start;
}
.bubble {
  max-width: 75%;
  padding: 8px 10px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
}
.msg.user .bubble {
  background: #667eea;
  color: #fff;
  border-radius: 18px 18px 4px 18px;
}
.msg.bot .bubble {
  background: #f0f0f0;
  color: #333;
  border-radius: 18px 18px 18px 4px;
}

/* 加载动画气泡 */
.bubble.loading {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
}
.bubble.loading span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #888;
  animation: bounce 1.4s infinite ease-in-out both;
}
.bubble.loading span:nth-child(1) {
  animation-delay: -0.32s;
}
.bubble.loading span:nth-child(2) {
  animation-delay: -0.16s;
}
@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.6;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 输入区 */
.input-row {
  display: flex;
  gap: 8px;
}
.input-field {
  flex: 1;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
  font-family: inherit;
}
.input-field:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
.input-field:disabled {
  background: #f5f5f5;
  color: #999;
}

.send-btn {
  padding: 10px 18px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  min-width: 70px;
}
.send-btn:hover:not(:disabled) {
  background: #5568d3;
}
.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 快捷提问 */
.quick {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.label {
  font-size: 14px;
  font-weight: 500;
}
.quick-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.quick-btn {
  padding: 6px 10px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: #fff;
  color: #667eea;
  font-size: 12px;
  cursor: pointer;
}
.quick-btn:hover:not(:disabled) {
  background: #667eea;
  color: #fff;
}
.quick-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 提示和清空按钮 */
.tips {
  font-size: 13px;
  color: #555;
  background: linear-gradient(135deg, #f0f4ff, #f9f5ff);
  border-left: 3px solid #667eea;
}
.tips p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.clear-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  font-size: 13px;
}
.clear-btn:hover {
  color: #5568d3;
}

@media (max-width: 640px) {
  .chat-window {
    max-height: 400px;
  }
  .bubble {
    max-width: 85%;
    font-size: 13px;
  }
  .send-btn {
    padding: 10px 14px;
    min-width: 60px;
    font-size: 13px;
  }
}
</style>
