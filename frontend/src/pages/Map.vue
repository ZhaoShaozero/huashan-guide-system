<template>
  <div class="map-page">
    <h2>华山核心景点导览</h2>
    <p class="subtitle">
      包含西峰、东峰、南峰、北峰、中峰以及长空栈道、苍龙岭等高风险路段。
    </p>


    <!-- 搜索和筛选 -->
    <div class="filters card">
      <input
        v-model="searchText"
        placeholder="🔍 搜索景点名称..."
        class="search-input"
      />
      <select v-model="filterDifficulty" class="filter-select">
        <option value="">全部难度</option>
        <option value="1-2">简单 (1-2)</option>
        <option value="3">中等 (3)</option>
        <option value="4-5">困难 (4-5)</option>
      </select>
      <select v-model="filterSafety" class="filter-select">
        <option value="">全部安全等级</option>
        <option value="safe">安全</option>
        <option value="medium">中等</option>
        <option value="danger">高危</option>
      </select>
    </div>


    <div v-if="loading" class="card">
      景点数据加载中…
    </div>


    <!-- 景点网格（固定3列） -->
    <div v-else class="grid">
      <div
        v-for="a in filteredAttractions"
        :key="a.id"
        class="card item"
        @click="selectAttraction(a)"
      >
        <h3>{{ a.name }}</h3>
        <p class="category">
          类型：{{ a.category }} · 海拔：{{ a.altitude || '—' }} m
        </p>
        <p class="desc">{{ a.description }}</p>
        <p class="meta">
          难度：{{ a.difficulty_level }}/5 · 预计游览：{{ a.estimated_time }} 分钟
        </p>
        <p class="safety" :class="safetyClass(a.safety_level)">
          安全等级：{{ a.safety_level || '未知' }}
        </p>
        <div class="actions">
          <button @click.stop="askExplain(a)">AI 讲解</button>
          <button @click.stop="safetyCheck(a)">安全检查</button>
        </div>
      </div>
    </div>


    <div v-if="filteredAttractions.length === 0 && !loading" class="card empty">
      未找到匹配的景点，请调整筛选条件。
    </div>


    <!-- AI 讲解结果 (带进度条) -->
    <div v-if="aiText || isGeneratingExplanation" class="card ai-box" ref="aiBoxRef">
      <h3>🤖 AI 景点讲解</h3>
      
      <!-- 正在生成 - 显示进度条 -->
      <div v-if="isGeneratingExplanation" class="loading-container">
        <div class="progress-bar">
          <div class="progress-fill"></div>
        </div>
        <p class="loading-text">正在生成讲解词...</p>
      </div>
      
      <!-- 已生成 - 显示内容 -->
      <p v-else class="explanation-text">{{ aiText }}</p>
      
      <button v-if="aiText" @click="aiText = ''" class="close-explanation">✕</button>
    </div>


    <!-- 景点详情弹窗 -->
    <div v-if="selectedAttr" class="modal" @click="selectedAttr = null">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="selectedAttr = null">✕</button>
        <h3>{{ selectedAttr.name }}</h3>


        <div class="detail-info">
          <p><strong>类别：</strong>{{ selectedAttr.category }}</p>
          <p><strong>海拔：</strong>{{ selectedAttr.altitude }} 米</p>
          <p><strong>难度等级：</strong>{{ selectedAttr.difficulty_level }}/5</p>
          <p><strong>预计游览时间：</strong>{{ selectedAttr.estimated_time }} 分钟</p>
          <p class="safety" :class="safetyClass(selectedAttr.safety_level)">
            <strong>安全等级：</strong>{{ selectedAttr.safety_level }}
          </p>
          <p><strong>描述：</strong></p>
          <p class="full-desc">{{ selectedAttr.description }}</p>


          <div v-if="selectedAttr.tips" class="tips-box">
            <p><strong>⚠️ 特别提示：</strong></p>
            <p>{{ selectedAttr.tips }}</p>
          </div>
        </div>


        <div class="modal-actions">
          <button class="btn primary" @click="askExplain(selectedAttr)">
            AI 讲解
          </button>
          <button class="btn" @click="safetyCheck(selectedAttr)">
            安全检查
          </button>
        </div>
      </div>
    </div>


    <!-- 安全检查弹窗 -->
    <div v-if="safetyCheckResult" class="modal" @click="safetyCheckResult = null">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="safetyCheckResult = null">✕</button>
        <h3>⚠️ 安全检查结果</h3>


        <div class="safety-result">
          <p class="location">
            <strong>景点：</strong>{{ safetyCheckResult.attraction_name }}
          </p>
          <p class="level">
            <strong>安全等级：</strong>
            <span :class="['badge', safetyCheckResult.safety_level]">
              {{ safetyCheckResult.safety_level }}
            </span>
          </p>


          <div v-if="safetyCheckResult.warnings.length > 0" class="warnings">
            <h4>⚠️ 针对您的警告：</h4>
            <ul>
              <li v-for="(w, idx) in safetyCheckResult.warnings" :key="idx">
                {{ w }}
              </li>
            </ul>
          </div>


          <div v-else class="safe-tip">
            ✓ 根据您的信息，该景点对您是安全的。
          </div>


          <div class="tips-box">
            <h4>💡 温馨提示：</h4>
            <p>{{ safetyCheckResult.tips }}</p>
          </div>
        </div>


        <div class="modal-actions">
          <button class="btn primary" @click="safetyCheckResult = null">
            了解
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'


// 改成你的后端地址
// const API_BASE = 'http://127.0.0.1:15500'
const API_BASE = ''


const attractions = ref([])
const loading = ref(true)
const aiText = ref('')
const isGeneratingExplanation = ref(false)
const selectedAttr = ref(null)
const safetyCheckResult = ref(null)
const aiBoxRef = ref(null)


const searchText = ref('')
const filterDifficulty = ref('')
const filterSafety = ref('')


onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/attractions`)
    attractions.value = res.data
  } catch (e) {
    console.error('获取景点失败', e)
  } finally {
    loading.value = false
  }
})


// 过滤后的景点列表
const filteredAttractions = computed(() => {
  let result = attractions.value


  // 按名称搜索
  if (searchText.value) {
    result = result.filter((a) =>
      a.name.toLowerCase().includes(searchText.value.toLowerCase()),
    )
  }


  // 按难度筛选
  if (filterDifficulty.value) {
    if (filterDifficulty.value === '1-2') {
      result = result.filter((a) => a.difficulty_level <= 2)
    } else if (filterDifficulty.value === '3') {
      result = result.filter((a) => a.difficulty_level === 3)
    } else if (filterDifficulty.value === '4-5') {
      result = result.filter((a) => a.difficulty_level >= 4)
    }
  }


  // 按安全等级筛选
  if (filterSafety.value) {
    if (filterSafety.value === 'safe') {
      result = result.filter((a) =>
        ['安全', '较安全'].includes(a.safety_level),
      )
    } else if (filterSafety.value === 'medium') {
      result = result.filter((a) => a.safety_level === '中等')
    } else if (filterSafety.value === 'danger') {
      result = result.filter((a) =>
        ['高危', '极端危险'].includes(a.safety_level),
      )
    }
  }


  return result
})


const safetyClass = (level) => {
  if (!level) return ''
  if (['安全', '较安全'].includes(level)) return 'safe'
  if (level === '中等') return 'medium'
  return 'danger'
}


const selectAttraction = (a) => {
  selectedAttr.value = a
}


const askExplain = async (a) => {
  // 显示加载状态
  isGeneratingExplanation.value = true
  aiText.value = ''
  selectedAttr.value = null
  
  // 立即滚动到讲解框（显示进度条）
  await new Promise(resolve => setTimeout(resolve, 50))
  if (aiBoxRef.value) {
    aiBoxRef.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
  
  try {
    const res = await axios.post(`${API_BASE}/api/ai/explain/${a.id}`, {
      audience_type: 'all',
    })
    // 延迟显示，给用户一种"生成完成"的感觉
    setTimeout(() => {
      aiText.value = res.data.explanation
      // 讲解词显示后不再滚动，保持在可视范围
    }, 300)
  } catch (e) {
    aiText.value = '暂时无法获取 AI 讲解，请稍后重试。'
    console.error('AI 讲解失败', e)
  } finally {
    isGeneratingExplanation.value = false
  }
}


const safetyCheck = async (a) => {
  try {
    // 这里 user_id 暂时写死为 1，后续接入登录系统后可替换
    const res = await axios.post(`${API_BASE}/api/safety-check`, {
      attraction_id: a.id,
      user_id: 1,
    })
    safetyCheckResult.value = res.data
    selectedAttr.value = null
  } catch (e) {
    console.error('安全检查失败', e)
    // fallback：至少给出基础提示
    safetyCheckResult.value = {
      attraction_id: a.id,
      attraction_name: a.name,
      safety_level: a.safety_level || '未知',
      warnings: [],
      tips:
        a.tips ||
        `${a.name} 的安全提示：请注意脚下安全，遵守景区指示，量力而行。`,
      can_proceed: true,
    }
  }
}
</script>


<style scoped>
.map-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.subtitle {
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
}
.card {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}


/* 筛选栏 */
.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.search-input,
.filter-select {
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}
.search-input {
  flex: 1;
  min-width: 180px;
}
.filter-select {
  min-width: 120px;
}
.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}


/* 空状态 */
.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}


/* 景点网格 - 固定3列 */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

/* 响应式处理 */
@media (max-width: 1200px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

.item {
  cursor: pointer;
  transition: all 0.2s ease;
}
.item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}
.item h3 {
  margin-bottom: 6px;
  font-size: 16px;
  color: #111;
}
.category {
  font-size: 12px;
  color: #777;
  margin-bottom: 6px;
}
.desc {
  font-size: 13px;
  color: #555;
  margin-bottom: 6px;
  line-height: 1.4;
}
.meta {
  font-size: 12px;
  color: #888;
  margin-bottom: 6px;
}
.safety {
  margin-top: 6px;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-block;
  font-weight: 500;
}
.safety.safe {
  background: #d4edda;
  color: #155724;
}
.safety.medium {
  background: #fff3cd;
  color: #856404;
}
.safety.danger {
  background: #f8d7da;
  color: #721c24;
}
.actions {
  margin-top: 10px;
  display: flex;
  gap: 6px;
}
.actions button {
  flex: 1;
  padding: 6px 10px;
  font-size: 12px;
  border: 1px solid #ddd;
  background: #f9f9f9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.actions button:hover {
  background: #f0f0f0;
  border-color: #999;
}


/* AI 讲解框 */
.ai-box {
  background: linear-gradient(135deg, #f0f4ff, #fff8e8);
  border-left: 4px solid #667eea;
  position: relative;
  padding-right: 40px;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.ai-box h3 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 16px;
}
.explanation-text {
  color: #555;
  line-height: 1.6;
  word-break: break-word;
  margin: 0;
}
.close-explanation {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  padding: 4px;
}
.close-explanation:hover {
  color: #333;
}


/* 加载进度条 */
.loading-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(102, 126, 234, 0.15);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  animation: progress-pulse 1.5s ease-in-out infinite;
  border-radius: 3px;
}

@keyframes progress-pulse {
  0% {
    width: 10%;
  }
  50% {
    width: 80%;
  }
  100% {
    width: 100%;
  }
}

.loading-text {
  text-align: center;
  color: #999;
  font-size: 13px;
  margin: 0;
  letter-spacing: 0.5px;
}


/* 模态框基础 */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}
.modal-content {
  background: #fff;
  border-radius: 10px;
  padding: 24px;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}
.close-btn:hover {
  color: #333;
}


/* 详情内容 */
.detail-info {
  margin-bottom: 16px;
  line-height: 1.8;
}
.detail-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #333;
}
.full-desc {
  background: #f9f9f9;
  padding: 10px;
  border-radius: 6px;
  margin-top: 4px;
  color: #555;
}
.tips-box {
  background: #fff9e6;
  border-left: 3px solid #ffa500;
  padding: 10px;
  border-radius: 4px;
  margin-top: 12px;
  font-size: 13px;
  color: #555;
}


/* 安全检查结果 */
.safety-result {
  margin-bottom: 16px;
}
.location,
.level {
  font-size: 14px;
  margin: 8px 0;
}
.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}
.badge.安全,
.badge.较安全 {
  background: #d4edda;
  color: #155724;
}
.badge.中等 {
  background: #fff3cd;
  color: #856404;
}
.badge.高危,
.badge.极端危险 {
  background: #f8d7da;
  color: #721c24;
}
.warnings {
  background: #fff5f5;
  border-left: 3px solid #d9534f;
  padding: 10px;
  border-radius: 4px;
  margin: 12px 0;
}
.warnings h4 {
  color: #d9534f;
  margin-bottom: 6px;
  font-size: 13px;
}
.warnings ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}
.warnings li {
  font-size: 13px;
  color: #666;
  margin: 4px 0;
  padding-left: 18px;
  position: relative;
}
.warnings li::before {
  content: '⚠️';
  position: absolute;
  left: 0;
}
.safe-tip {
  background: #d4edda;
  border-left: 3px solid #28a745;
  padding: 10px;
  border-radius: 4px;
  margin: 12px 0;
  font-size: 13px;
  color: #155724;
}
.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.btn {
  padding: 8px 14px;
  border: 1px solid #ddd;
  background: #fff;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.15s ease;
  flex: 1;
}
.btn:hover {
  background: #f0f0f0;
  border-color: #999;
}
.btn.primary {
  background: #667eea;
  color: #fff;
  border-color: #667eea;
}
.btn.primary:hover {
  background: #5568d3;
  border-color: #5568d3;
}
</style>