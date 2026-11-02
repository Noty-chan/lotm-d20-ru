import { defineConfig } from 'vitepress'
const chapters = ['Предисловие','Проверки','Характеристики','Навыки и профессии','Стать Потусторонним','Бой','Особые дополнения','Потусторонние предметы','Ритуальная магия']
const paths = ['Дурака · Провидец','Ученика','Ошибки · Мародёр (Вор)','Мечтателя · Зритель','Тирана · Матрос (Моряк)','Солнца · Бард','Читателя','Повешенного · Искатель Секретов (Тайномолец; Проситель Секретов)','Смерти · Собиратель Трупов','Ночи · Бессонный','Бога Войны · Воин','Чёрного Императора · Адвокат','Судьи · Арбитр','Красного Жреца · Охотник','Ведьмы · Убийца','Бездны · Преступник','Нелюдя · Заключённый (Узник)','Жреца Тайн','Совершенного · Савант (Всезнайка)','Луны · Аптекарь','Земли · Земледелец','Судьбы · Монстр']
const baseInput = process.env.READER_BASE || '/'
const base = '/' + baseInput.split('/').filter(Boolean).join('/') + (baseInput.split('/').filter(Boolean).length ? '/' : '')
export default defineConfig({
  lang: 'ru-RU', title: 'Повелитель Тайн — правила', description: 'Рабочий перевод китайской НРИ', base,
  cleanUrls: true, lastUpdated: false, ignoreDeadLinks: false,
  markdown: { html: false },
  themeConfig: {
    search: { provider: 'local', options: { locales: { root: { translations: { button: { buttonText: 'Поиск', buttonAriaLabel: 'Поиск по книге' }, modal: { noResultsText: 'Ничего не найдено', resetButtonTitle: 'Очистить', footer: { selectText: 'выбрать', navigateText: 'перейти', closeText: 'закрыть' } } } } } } },
    nav: [{text:'Главная',link:'/'},{text:'Моё чтение',link:'/reader'},{text:'Начать чтение',link:'/book/chapter-01'}],
    sidebar: [
      {text:'Главы 1–9',collapsed:true,items:chapters.map((text,i)=>({text:`${i+1}. ${text}`,link:`/book/chapter-${String(i+1).padStart(2,'0')}`}))},
      {text:'Пути',collapsed:true,items:paths.map((name,i)=>({text:`${i+1}. Путь ${name}`,link:`/book/chapter-10-${String(i+1).padStart(2,'0')}`}))},
      {text:'Главы 11–15',collapsed:true,items:[{text:'11. Проявление формы мифического существа',link:'/book/chapter-11'},{text:'12. Особые области',link:'/book/chapter-12'},{text:'13. Сверхъестественные существа',link:'/book/chapter-13'},{text:'14. Дневник Скрытого Мудреца',link:'/book/chapter-14'},{text:'15. Смена Последовательности',link:'/book/chapter-15'},{text:'Дополнительные материалы',link:'/book/appendices'}]}
    ],
    outline: { level: [2, 3], label: 'На этой странице' },
    docFooter: { prev: 'Назад', next: 'Далее' }, returnToTopLabel: 'Наверх', sidebarMenuLabel: 'Оглавление', darkModeSwitchLabel: 'Тема'
  }
})
