<template>
  <div class="routes-page">
    <h2>你的华山推荐路线</h2>

    <div v-if="route" class="card">
      <h3>{{ route.name }}</h3>
      <p class="tag">
        难度：{{ route.difficulty }} · 预计用时：{{ route.estimated_duration }} 分钟
      </p>
      <p class="tag">适合人群：{{ route.recommended_for }}</p>
      <p class="tag">索道方案：{{ route.cable_car_usage }}</p>

      <h4>路线说明</h4>
      <p class="desc">{{ route.description }}</p>

      <h4>包含景点（按顺序）</h4>
      <ol class="poi-list">
        <li v-for="n in route.attractions" :key="n">
          编号：{{ n }}（可在“景点列表”中查看详细介绍）
        </li>
      </ol>

      <div class="note">
        注：实际开放时间、票价、索道运营情况请以华山景区官方公告为准，本系统为演示用智慧导览原型。
      </div>
    </div>

    <div v-else class="card">
      暂无推荐路线，请先在首页使用“智能推荐路线”功能填写你的体力和偏好。
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const route = ref(null)

onMounted(() => {
  const data = localStorage.getItem('recommendedRoute')
  if (data) {
    route.value = JSON.parse(data)
  }
})
</script>

<style scoped>
.routes-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.card {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
}
.tag {
  font-size: 14px;
  color: #555;
}
.desc {
  margin: 8px 0;
}
.poi-list {
  padding-left: 20px;
}
.poi-list li {
  margin: 4px 0;
}
.note {
  margin-top: 10px;
  font-size: 12px;
  color: #777;
}
</style>
