export const BOOKMARKS = 'lotm-d20-ru:bookmarks:v1'
export const LAST = 'lotm-d20-ru:last:v1'
export function load(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key) || 'null') ?? fallback } catch { return fallback }
}
export function save(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); return true } catch { return false }
}
