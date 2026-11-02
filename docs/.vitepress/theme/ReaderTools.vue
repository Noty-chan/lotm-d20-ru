<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useData, useRoute, withBase } from 'vitepress'
import { BOOKMARKS, LAST, load, save } from './reading.js'
const { page } = useData()
const route = useRoute()
const message = ref('')
let timer
function place() {
  const headings = Array.from(document.querySelectorAll('.vp-doc h2[id], .vp-doc h3[id]'))
  const heading = headings.filter(h => h.getBoundingClientRect().top < innerHeight * 0.4).at(-1)
  const title = page.value.title || 'Повелитель Тайн — правила'
  const section = heading?.textContent?.replace(/\s*#\s*$/, '').trim()
  return { url: location.pathname + (heading ? '#' + encodeURIComponent(heading.id) : ''), title: section ? `${title} · ${section}` : title, time: Date.now() }
}
function remember() {
  if (!page.value.relativePath.startsWith('book/')) return
  save(LAST, place())
}
function scroll() { clearTimeout(timer); timer = setTimeout(remember, 250) }
function bookmark() {
  const current = place()
  const items = load(BOOKMARKS, [])
  const exists = items.some(i => i.url === current.url)
  const ok = save(BOOKMARKS, [current, ...items.filter(i => i.url !== current.url)])
  message.value = ok ? (exists ? 'Закладка обновлена' : 'Закладка сохранена') : 'Браузер не разрешил сохранить закладку'
}
watch(() => route.path, async () => { message.value = ''; await nextTick(); clearTimeout(timer); timer = setTimeout(remember, 500) })
onMounted(() => { timer = setTimeout(remember, 500); window.addEventListener('scroll', scroll, { passive: true }); window.addEventListener('pagehide', remember) })
onUnmounted(() => { clearTimeout(timer); window.removeEventListener('scroll', scroll); window.removeEventListener('pagehide', remember) })
</script>
<template>
  <div v-if="page.relativePath.startsWith('book/')" class="reader-tools">
    <button type="button" @click="bookmark">☆ В закладки</button>
    <a :href="withBase('/reader')">Моё чтение →</a>
    <span role="status" aria-live="polite">{{ message }}</span>
  </div>
</template>
