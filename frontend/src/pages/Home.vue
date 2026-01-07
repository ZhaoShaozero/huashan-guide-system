<template>
  <div class="home">
    <!-- 顶部介绍卡片 -->
    <section class="card hero">
      <h2>华山慧行 · 智慧安全导览</h2>
      <p>
        面向不同游客人群，提供华山一站式智慧导览服务：路线推荐、安全预警、景点讲解与 AI 智能问答。
      </p>
      <div class="hero-buttons">
        <button class="btn primary" @click="showForm = true">🧭 智能推荐路线</button>
        <button class="btn" @click="go('/map')">🗺️ 查看景点分布</button>
        <button class="btn" @click="go('/ai-chat')">🤖 AI 问华山</button>
      </div>
    </section>

    <!-- 今日信息 -->
    <section class="card info">
      <h3>今日提示</h3>
      <ul>
        <li>建议提前关注华山景区官网的天气和索道运行公告。</li>
        <li>体力一般游客可优先考虑“西上北下”或“西峰往返”路线。</li>
        <li>恐高或有心血管疾病人群不建议体验长空栈道、鹞子翻身等高风险项目。</li>
      </ul>
    </section>

    <!-- 功能一览 -->
    <section class="card">
      <h3>你可以在这里做什么？</h3>
      <ul class="feature-list">
        <li>🎯 根据体力、恐高与健康情况，生成专属登山路线。</li>
        <li>🗺️ 快速浏览华山核心景点的难度、安全等级与游览时间。</li>
        <li>🤖 和 AI 导游对话，获取游玩建议、路线参考与安全提醒。</li>
      </ul>
    </section>

    <!-- 推荐结果展示（如果有） -->
    <div v-if="recommendedRoute" class="card success-box">
      <h3>✓ 为您推荐的路线</h3>
      <div class="route-result">
        <p><strong>路线名称：</strong>{{ recommendedRoute.name }}</p>
        <p><strong>难度等级：</strong>{{ getDifficultyLabel(recommendedRoute.difficulty) }}</p>
        <p><strong>预计耗时：</strong>{{ recommendedRoute.estimated_duration }} 分钟</p>
        <p><strong>推荐人群：</strong>{{ recommendedRoute.recommended_for }}</p>
        <p><strong>路线描述：</strong>{{ recommendedRoute.description }}</p>
        <p><strong>缆车方案：</strong>{{ recommendedRoute.cable_car_usage }}</p>
        <div class="route-actions">
          <button class="btn primary" @click="go('/routes')">查看详细路线</button>
          <button class="btn" @click="clearRecommendation">重新推荐</button>
        </div>
      </div>
    </div>

    <!-- 智能推荐表单弹窗 -->
    <div v-if="showForm" class="modal">
      <div class="modal-body card">
        <button class="close-btn" @click="showForm = false">✕</button>
        <h3>填写你的出行情况</h3>

        <label>
          你的姓名：
          <input
            v-model="form.username"
            type="text"
            placeholder="可选，用于个性化服务"
          />
        </label>

        <label>
          年龄段：
          <select v-model="form.age_group">
            <option value="">-- 请选择 --</option>
            <option value="minor">未成年不建议</option>
            <option value="20-30">20-30 岁</option>
            <option value="30-40">30-40 岁</option>
            <option value="40-50">40-50 岁</option>
            <option value="50+">50 岁以上</option>
          </select>
        </label>

        <label>
          体力情况：
          <select v-model="form.fitness_level">
            <option value="">-- 请选择 --</option>
            <option value="weak">较弱（容易疲劳）</option>
            <option value="normal">一般（可以走一段）</option>
            <option value="good">较好（能走长距离）</option>
          </select>
        </label>

        <label class="checkbox">
          <input type="checkbox" v-model="form.fear_of_heights" />
          我有明显恐高
        </label>

        <label class="checkbox">
          <input type="checkbox" v-model="form.has_medical_condition" />
          我有心脏病 / 高血压等情况
        </label>

        <div class="actions">
          <button
            class="btn primary"
            @click="submit"
            :disabled="loading || !formValid"
          >
            {{ loading ? '生成中…' : '生成推荐路线' }}
          </button>
          <button class="btn" @click="showForm = false" :disabled="loading">
            取消
          </button>
        </div>

        <p v-if="error" class="error">⚠️ {{ error }}</p>
        <p v-if="successMsg" class="success">✓ {{ successMsg }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const showForm = ref(false)
const loading = ref(false)
const error = ref('')
const successMsg = ref('')
const recommendedRoute = ref(null)

// 注意：改成你的后端地址和端口
// const API_BASE = 'http://127.0.0.1:15500'
const API_BASE = ''

const form = ref({
  username: '',
  age_group: '',
  fitness_level: 'normal',
  fear_of_heights: false,
  has_medical_condition: false,
})

// 表单验证：年龄段 + 体力必填
const formValid = computed(() => {
  return form.value.age_group && form.value.fitness_level
})

const go = (path) => router.push(path)

const getDifficultyLabel = (difficulty) => {
  const labels = {
    easy: '简单 ⭐',
    medium: '中等 ⭐⭐⭐',
    hard: '困难 ⭐⭐⭐⭐⭐',
  }
  return labels[difficulty] || difficulty || '未知'
}

// 清除推荐结果
const clearRecommendation = () => {
  recommendedRoute.value = null
  localStorage.removeItem('recommendedRoute')
  showForm.value = true
}

// 如果 localStorage 里已经有推荐结果，初始化显示一下
onMounted(() => {
  const saved = localStorage.getItem('recommendedRoute')
  if (saved) {
    try {
      recommendedRoute.value = JSON.parse(saved)
    } catch {
      // ignore parse error
    }
  }
})

const submit = async () => {
  error.value = ''
  successMsg.value = ''
  if (!formValid.value) {
    error.value = '请先选择年龄段和体力情况。'
    return
  }

  loading.value = true

  try {
    const res = await axios.post(`/api/routes/recommend`, {
      age_group: form.value.age_group,
      fitness_level: form.value.fitness_level,
      fear_of_heights: form.value.fear_of_heights,
      has_medical_condition: form.value.has_medical_condition,
    })

    if (res.data && res.data.recommended_route) {
      recommendedRoute.value = res.data.recommended_route
      localStorage.setItem(
        'recommendedRoute',
        JSON.stringify(res.data.recommended_route),
      )
      successMsg.value = `推荐完成！已为您推荐“${res.data.recommended_route.name}”路线`
      showForm.value = false
      setTimeout(() => {
        successMsg.value = ''
      }, 3000)
    } else {
      error.value = '未获取到推荐路线，请稍后重试。'
    }
  } catch (e) {
    console.error('推荐请求错误：', e)
    error.value =
      e.response?.data?.error || '请求失败，请检查网络或后端服务。'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 卡片基础样式：柔和浅色系 */
.card {
  background: #f9fafb;
  border-radius: 10px;
  padding: 16px 18px;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06);
  border: 1px solid #e5e7eb;
}

/* 顶部大卡片 */
.hero {
  background: linear-gradient(135deg, #e0ecff, #f3f4ff);
}
.hero h2 {
  margin-bottom: 8px;
  font-size: 22px;
  color: #111827;
}
.hero p {
  margin-bottom: 12px;
  color: #4b5563;
}
.hero-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 信息卡片 */
.info ul {
  padding-left: 18px;
  color: #4b5563;
}
.info li {
  margin: 4px 0;
}

/* 功能列表 */
.feature-list {
  padding-left: 18px;
  color: #4b5563;
}
.feature-list li {
  margin: 4px 0;
}

/* 推荐结果卡片 */
.success-box {
  background: linear-gradient(135deg, #d4edda, #e8f5e9);
  border-left: 4px solid #28a745;
}
.route-result {
  line-height: 1.8;
  color: #333;
}
.route-result p {
  margin: 6px 0;
  font-size: 14px;
}
.route-result strong {
  color: #155724;
}
.route-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

/* 按钮样式：圆角、浅色 */
.btn {
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}
.btn.primary {
  border-color: #4f46e5;
  background: #4f46e5;
  color: #f9fafb;
}
.btn.primary:hover:not(:disabled) {
  background: #4338ca;
  border-color: #3730a3;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 弹窗 */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}
.modal-body {
  width: 360px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

/* 右上角关闭按钮 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #9ca3af;
}
.close-btn:hover {
  color: #4b5563;
}

/* 表单 */
label {
  display: block;
  margin: 10px 0;
  font-size: 14px;
  color: #374151;
}
select,
input[type='text'] {
  width: 100%;
  margin-top: 4px;
  padding: 6px 8px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background: #fff;
  font-size: 14px;
  font-family: inherit;
}
select:focus,
input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
.checkbox {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 8px 0;
}
.checkbox input {
  width: auto;
  margin-top: 0;
}
.actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}
.actions .btn {
  flex: 1;
}
.error {
  margin-top: 8px;
  font-size: 13px;
  color: #b91c1c;
}
.success {
  margin-top: 8px;
  font-size: 13px;
  color: #15803d;
}
</style>
