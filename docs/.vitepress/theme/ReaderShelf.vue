<script setup>
import { ref, onMounted } from 'vue'
import { useData } from 'vitepress'
import { BOOKMARKS, LAST, load, save } from './reading.js'
const { page } = useData()
const last = ref(null)
const items = ref([])
onMounted(() => { last.value = load(LAST, null); items.value = load(BOOKMARKS, []) })
function remove(url) { const next = items.value.filter(i => i.url !== url); if (save(BOOKMARKS, next)) items.value = next }
</script>
<template>
  <div v-if="page.relativePath === 'reader.md'" class="reader-shelf vp-doc">
    <h2>Продолжить чтение</h2>
    <p v-if="last"><a :href="last.url">{{ last.title }} →</a></p>
    <p v-else>Откройте любую главу, и здесь появится место, где вы остановились.</p>
    <h2>Закладки</h2>
    <p v-if="!items.length">Закладок пока нет. Их можно добавить в начале любой страницы книги.</p>
    <ul v-else class="bookmark-list"><li v-for="item in items" :key="item.url"><a :href="item.url">{{ item.title }}</a><button type="button" @click="remove(item.url)" :aria-label="`Удалить закладку ${item.title}`">Удалить</button></li></ul>
    <p class="reader-note">Место чтения и закладки хранятся в этом браузере на этом устройстве.</p>
  </div>
</template>
