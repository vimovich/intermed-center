#!/usr/bin/env python3
"""Generates INTERMED CENTER pages + partials from shared data."""
import json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

# ---------------- icons ----------------
I = {
 'arr': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 'left': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
 'right': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2" stroke-linecap="round"/></svg>',
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3.5" y="5.5" width="17" height="13" rx="3"/><path d="M4 7.5l8 5.5 8-5.5" stroke-linejoin="round"/></svg>',
 'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3.5" y="5" width="17" height="15" rx="3.5"/><path d="M3.5 10h17M8 3v4M16 3v4" stroke-linecap="round"/><circle cx="12" cy="15" r="1.4" fill="currentColor"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'flask': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5.5 9.2A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.8L14 9V3"/><path d="M7 15h10"/></svg>',
 'wave': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 12c2-4 4-4 6 0s4 4 6 0 3-3 4-1"/><path d="M4 17c2-2 4-2 6 0M4 7c2-2 4-2 6 0"/></svg>',
 'ecg': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-5 3 10 2.5-7 1.5 2h5"/></svg>',
 'scan': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16M4 12h16"/></svg>',
 'drop': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0c0-4.1 6-10.5 6-10.5z"/></svg>',
 'doc': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M7 3h7l5 5v12a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v5h5M9 13h6M9 17h6" stroke-linecap="round"/></svg>',
 'tg': '<svg viewBox="0 0 24 24"><path d="M21.5 4.3 2.9 11.5c-1 .4-1 1.2-.2 1.5l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.4l2.2-2.1 4.6 3.4c.8.5 1.4.2 1.6-.8l3-14.3c.3-1.3-.5-1.9-1.5-1.4zM9.9 14.2l-.4 4-1.5-4.8L18.4 7z" fill="currentColor"/></svg>',
 'wa': '<svg viewBox="0 0 24 24"><path d="M12 3.2a8.8 8.8 0 0 0-7.6 13.2L3.2 20.8l4.5-1.2A8.8 8.8 0 1 0 12 3.2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 8.3c.2-.4.4-.4.7-.4h.5c.2 0 .4 0 .5.4l.7 1.6c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5.4.7 1 1.4 1.7 1.9.6.4 1 .6 1.2.7.2.1.3 0 .5-.1l.6-.8c.2-.2.4-.2.6-.1l1.5.7c.2.1.4.2.4.4 0 .5-.1 1.1-.6 1.5-.5.4-1.4.7-2.4.4a9 9 0 0 1-5.3-4.7c-.4-1-.4-2.1.5-3.2z" fill="currentColor"/></svg>',
 'ig': '<svg viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor"/></svg>',
 'x': '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 'plus': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
 'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5a6.5 6.5 0 0 1 3.5 5.5"/></svg>',
}
def btn(label, cls='btn--grad', attrs='', icon='up', tag='button', href=None):
    a = f' href="{href}"' if href else (' type="button"' if tag == 'button' else '')
    return f'<{tag} class="btn {cls}"{a} {attrs}>{label}<span class="btn__i">{I[icon]}</span></{tag}>'

IMG = lambda id, w, h=None: f'IMG({id},{w}' + (f',{h})' if h else ')')

# ---------------- data ----------------
TEL, TEL_H = '+998712000000', '+998 71 200-00-00'
ADDR = 'Ташкент, Мирзо-Улугбекский район, ул. Буюк Ипак Йули, 12'
HOURS = 'Пн–Сб 8:00–20:00, Вс 9:00–15:00'

DIRS = [
 dict(id='terapiya', icon='cross', c='#0fb3a6', t='Терапия и гастроэнтерология', d='Диагностика и лечение заболеваний внутренних органов, ведение хронических болезней, коррекция питания.', price='150 000', srv=[('Приём терапевта','150 000'),('Повторный приём','120 000'),('Приём гастроэнтеролога','200 000'),('Капельница (без препарата)','120 000'),('Справка 086/у','250 000'),('Ведение хронического пациента, месяц','900 000')]),
 dict(id='kardiologiya', icon='heart', c='#ff5d55', t='Кардиология', d='Обследование и лечение сердца и сосудов: ЭКГ, ЭхоКГ, суточный Холтер, контроль давления.', price='200 000', srv=[('Приём кардиолога','200 000'),('ЭКГ с расшифровкой','80 000'),('ЭхоКГ (УЗИ сердца)','300 000'),('Холтер ЭКГ, 24 часа','350 000'),('СМАД, 24 часа','300 000'),('Дуплекс сосудов шеи','280 000')]),
 dict(id='ginekologiya', icon='venus', c='#f47fae', t='Гинекология', d='Женское здоровье на всех этапах: профилактика, лечение, планирование и ведение беременности.', price='200 000', srv=[('Приём гинеколога','200 000'),('УЗИ органов малого таза','180 000'),('Кольпоскопия','250 000'),('Ведение беременности, триместр','2 400 000'),('Мазок на онкоцитологию','120 000'),('Установка ВМС','450 000')]),
 dict(id='urologiya', icon='kidney', c='#f08a7a', t='Урология и андрология', d='Заболевания мочеполовой системы и почек у мужчин и женщин, мужское репродуктивное здоровье.', price='200 000', srv=[('Приём уролога','200 000'),('УЗИ почек и мочевого пузыря','160 000'),('УЗИ простаты (ТРУЗИ)','220 000'),('Урофлоуметрия','150 000'),('Спермограмма','230 000'),('Инстилляция мочевого пузыря','200 000')]),
 dict(id='nevrologiya', icon='neuron', c='#9b8cff', t='Неврология', d='Головные боли, головокружения, боли в спине, нарушения сна, восстановление после инсульта.', price='200 000', srv=[('Приём невролога','200 000'),('ЭЭГ','260 000'),('УЗДГ сосудов головы','280 000'),('Блокада (без препарата)','180 000'),('Курс реабилитации, 10 сеансов','1 800 000'),('Консультация по сну','220 000')]),
 dict(id='endokrinologiya', icon='molecule', c='#2fbfd0', t='Эндокринология', d='Щитовидная железа, сахарный диабет, гормональный фон, обмен веществ и контроль веса.', price='200 000', srv=[('Приём эндокринолога','200 000'),('УЗИ щитовидной железы','150 000'),('Гормоны щитовидной железы (ТТГ, Т4)','160 000'),('Гликированный гемоглобин','90 000'),('Программа снижения веса, 3 мес.','2 900 000'),('Помповая инсулинотерапия — консультация','300 000')]),
 dict(id='uzi', icon='drop', c='#4bd0c3', t='УЗИ и функциональная диагностика', d='Экспертное УЗИ всех органов, допплерография, ЭКГ и суточные мониторинги за один визит.', price='150 000', srv=[('УЗИ брюшной полости','180 000'),('УЗИ щитовидной железы','150 000'),('УЗИ молочных желёз','170 000'),('УЗИ суставов (1 сустав)','160 000'),('Допплер вен нижних конечностей','300 000'),('Комплексное УЗИ «Check»','490 000')]),
 dict(id='laboratoriya', icon='tube', c='#0fb3a6', t='Лабораторная диагностика', d='Более 400 видов анализов, собственный процедурный кабинет и результаты онлайн — от 2 часов.', price='35 000', srv=[('Общий анализ крови','45 000'),('Биохимия, 12 показателей','210 000'),('Витамин D','150 000'),('Ферритин','80 000'),('Коагулограмма','120 000'),('Забор крови','35 000')]),
]
DOCS = [
 dict(img='1678695972687-033fa0bdbac9', n='Дилноза Рахимова', r='Терапевт · Гастроэнтеролог', xp='14 лет', tags=['Терапия','Гастроэнтерология','Нутрициология'], d='terapiya'),
 dict(img='1666887360369-1901f341fdad', n='Бахтиёр Усманов', r='Кардиолог · Функциональная диагностика', xp='22 года', tags=['Кардиология','ЭхоКГ','Холтер'], d='kardiologiya'),
 dict(img='1757125736482-328a3cdd9743', n='Нигора Каримова', r='Гинеколог · Врач УЗИ', xp='16 лет', tags=['Гинекология','УЗИ','Беременность'], d='ginekologiya'),
 dict(img='1645066928295-2506defde470', n='Шерзод Алиев', r='Уролог · Андролог', xp='12 лет', tags=['Урология','Андрология'], d='urologiya'),
 dict(img='1622902046580-2b47f47f5471', n='Азамат Юлдашев', r='Невролог', xp='10 лет', tags=['Неврология','ЭЭГ','Реабилитация'], d='nevrologiya'),
 dict(img='1623854767648-e7bb8009f0db', n='Малика Турсунова', r='Эндокринолог', xp='9 лет', tags=['Эндокринология','Диабет','Щитовидная железа'], d='endokrinologiya'),
]
CHECKS = [
 dict(icon='cross', t='«Ежегодное обследование»', s='для мужчин и женщин', items=['Общий и биохимический анализ крови','ЭКГ и УЗИ брюшной полости','Приём терапевта с заключением'], n=14, p='690 000', old=None, b=None),
 dict(icon='venus', t='«Планирование беременности»', s='парное — для неё и для него', items=['Гормоны, инфекции, генетика','УЗИ малого таза, спермограмма','Консультации гинеколога и уролога'], n=32, p='2 400 000', old='2 650 000', b='−10%', hot=True),
 dict(icon='heart', t='«Кардиориск»', s='для мужчин и женщин 35+', items=['Липидный профиль, глюкоза','ЭКГ, ЭхоКГ, СМАД','Приём кардиолога'], n=11, p='890 000', old='1 050 000', b='−15%'),
 dict(icon='neuron', t='«Головные боли»', s='для мужчин и женщин', items=['УЗДГ сосудов головы и шеи','ЭЭГ, анализы крови','Приём невролога'], n=9, p='780 000', old=None, b=None),
 dict(icon='molecule', t='«Хроническая усталость»', s='для мужчин и женщин', items=['Гормоны щитовидной железы, витамины','Ферритин, витамин D, B12','Приём эндокринолога и терапевта'], n=21, p='1 900 000', old='2 100 000', b='−10%'),
 dict(icon='kidney', t='«Мужское здоровье»', s='для мужчин 30+', items=['ПСА, тестостерон, спермограмма','УЗИ почек и простаты','Приём уролога-андролога'], n=13, p='950 000', old=None, b=None),
]
FAQ = [
 ('Как записаться на приём к врачу?', 'Позвоните нам, напишите в Telegram или оставьте заявку на сайте — администратор перезвонит в течение 15 минут и подберёт удобное время.'),
 ('Принимаете ли вы пациентов без записи?', 'Да, при наличии свободного времени у врача. Чтобы не ждать, рекомендуем записаться заранее — приём идёт строго по времени.'),
 ('Какие методы диагностики у вас доступны?', 'УЗИ экспертного класса, ЭКГ, ЭхоКГ, суточный Холтер и СМАД, ЭЭГ, допплерография и собственная лаборатория — более 400 видов анализов.'),
 ('Как подготовиться к визиту и анализам?', 'Большинство анализов крови сдаются натощак, с 8:00 до 11:00. Перед УЗИ брюшной полости не ешьте 6–8 часов. Подробную памятку пришлём после записи.'),
 ('Можно ли получить результаты анализов онлайн?', 'Да. Результаты приходят в Telegram или на e-mail — большинство готовы в течение дня, экспресс-анализы от 2 часов.'),
 ('Есть ли у клиники лицензия?', 'Клиника работает на основании лицензии Министерства здравоохранения Республики Узбекистан. Копии документов доступны на странице «О центре».'),
]
POSTS = [
 dict(img='1631217868264-e5b90bb7e133', cat='Профилактика', date='12.10.2026', t='Симптомы, которые нельзя игнорировать', d='Когда стоит не откладывать визит к врачу и какие сигналы организма требуют внимания.'),
 dict(img='1606206591513-adbfbdd7a177', cat='Анализы', date='05.10.2026', t='Чек-ап раз в год: какие анализы действительно нужны', d='Разбираем базовый набор исследований для взрослых и как часто их стоит повторять.'),
 dict(img='1758691462123-8a17ae95d203', cat='Кардиология', date='28.09.2026', t='Давление «скачет»: как найти причину', d='Почему важно суточное мониторирование и что поможет держать давление под контролем.'),
 dict(img='1602052577122-f73b9710adba', cat='Лаборатория', date='20.09.2026', t='Как правильно сдавать кровь', d='Простые правила подготовки, которые сделают результаты анализов точными.'),
 dict(img='1758691462126-2ee47c8bf9e7', cat='Семья', date='14.09.2026', t='Здоровье всей семьи в одной клинике', d='Как составить план профилактических осмотров для детей, родителей и бабушек с дедушками.'),
 dict(img='1790315978536-70bff5474d71', cat='УЗИ', date='02.09.2026', t='УЗИ без мифов: безопасно ли и как часто можно', d='Отвечаем на частые вопросы пациентов об ультразвуковой диагностике.'),
]
GALLERY = [('1776886099265-6366478b341b','Зона ожидания'),('1606206591513-adbfbdd7a177','Лаборатория'),('1759987383760-327efaf5522a','Холл клиники'),('1758691461935-202e2ef6b69f','Кабинет врача'),('1637665759389-41818b867562','Процедурный кабинет'),('1779281887548-f676406dea2f','Комфортное ожидание'),('1602052577122-f73b9710adba','Диагностика')]
NAV = [('/', 'Главная'), ('/napravleniya', 'Направления'), ('/vrachi', 'Врачи'), ('/check-up', 'Чек-апы'), ('/ceny', 'Цены'), ('/o-centre', 'О центре'), ('/blog', 'Блог'), ('/kontakty', 'Контакты')]

# ---------------- partials ----------------
LOGO = f'<a class="logo" href="/" aria-label="INTERMED CENTER — на главную"><span class="logo__mark">{I["plus"]}</span><span class="logo__t"><b>INTERMED</b><small>center · клиника</small></span></a>'
HEAD = '''<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="theme-color" content="#f7fbfb" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preconnect" href="https://images.unsplash.com" />
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&family=Unbounded:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/src/css/main.css" />'''
navlinks = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)
HEADER = f'''<a class="skip" href="#main">К основному контенту</a>
<header class="hdr" data-hdr><div class="container hdr__in">{LOGO}
<nav class="nav" aria-label="Основная навигация">{navlinks}</nav>
<div class="hdr__act"><a class="hdr__tel" href="tel:{TEL}"><b>{TEL_H}</b><span>{HOURS.split(",")[0]}</span></a>
{btn("Записаться", "btn--ink btn--sm", "data-book", "up")}
<button class="burger" data-burger aria-label="Меню" aria-expanded="false"><i></i><i></i></button></div></div></header>
<div class="mnav" data-mnav aria-hidden="true"><nav class="mnav__links" aria-label="Мобильное меню">{navlinks}</nav>
<div class="mnav__foot"><a class="t" href="tel:{TEL}">{TEL_H}</a><p>{ADDR}<br>{HOURS}</p>{btn("Записаться на приём", "btn--grad btn--block", "data-book")}</div></div>'''
opts = ''.join(f'<option>{E(d["t"])}</option>' for d in DIRS)
FOOTER = f'''<footer class="ftr"><div class="container">
<div class="ftr__top">
 <div class="ftr__brand">{LOGO}<p>Многопрофильный медицинский центр: диагностика, лечение и профилактика для всей семьи в одной клинике.</p>
  <div class="soc"><a href="https://t.me/" target="_blank" rel="noopener" aria-label="Telegram">{I["tg"]}</a><a href="https://instagram.com/" target="_blank" rel="noopener" aria-label="Instagram">{I["ig"]}</a><a href="https://wa.me/998712000000" target="_blank" rel="noopener" aria-label="WhatsApp">{I["wa"]}</a></div></div>
 <nav class="ftr__nav" aria-label="Меню"><p class="ftr__h">Меню</p><a href="/napravleniya">Направления</a><a href="/vrachi">Врачи</a><a href="/check-up">Чек-апы</a><a href="/ceny">Цены</a><a href="/o-centre">О центре</a><a href="/blog">Блог</a></nav>
 <nav class="ftr__nav" aria-label="Направления"><p class="ftr__h">Направления</p>{"".join(f'<a href="/napravleniya#{d["id"]}">{E(d["t"].split(" и ")[0])}</a>' for d in DIRS[:6])}</nav>
 <div class="ftr__c"><p class="ftr__h">Контакты</p><a class="t" href="tel:{TEL}">{TEL_H}</a><p>{ADDR}<br>{HOURS}</p>{btn("Заказать звонок", "btn--grad btn--sm", "data-book")}</div>
</div>
<div class="ftr__legal"><p>ООО «INTERMED CENTER». Лицензия Министерства здравоохранения Республики Узбекистан на осуществление медицинской деятельности.</p><p>Информация на сайте носит ознакомительный характер и не является публичной офертой. Окончательный объём и стоимость услуг определяются после очной консультации специалиста. Имеются противопоказания, необходима консультация специалиста.</p></div>
<div class="ftr__bot"><span>© 2026 INTERMED CENTER</span><a href="/kontakty#privacy">Политика обработки персональных данных</a><span>Многопрофильный медицинский центр · Ташкент</span></div>
<div class="ftr__big" aria-hidden="true">INTERMED</div>
</div></footer>
<button class="fab" data-book aria-label="Записаться на приём">Запись</button>
<div class="modal" data-modal aria-hidden="true"><div class="modal__bg" data-close></div>
<div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="mtitle">
<button class="modal__x" data-close aria-label="Закрыть">{I["x"]}</button>
<div class="modal__aside"><span class="kicker">Онлайн-запись</span><h3 id="mtitle">Запись на приём к врачу</h3><p>Оставьте заявку — администратор перезвонит в течение 15 минут и подберёт удобное время и специалиста.</p><img src="/img/3d/capsule.webp" alt="" width="560" height="560" /></div>
<form class="form" data-form novalidate>
 <label class="fld"><span>Ваше имя</span><input name="name" required autocomplete="name" placeholder="Как к вам обращаться" /></label>
 <label class="fld"><span>Телефон</span><input name="phone" type="tel" required inputmode="tel" autocomplete="tel" placeholder="+998 __ ___-__-__" /></label>
 <label class="fld"><span>Направление</span><select name="dir"><option value="">Не знаю — нужна консультация</option>{opts}<option>Чек-ап (комплексное обследование)</option></select></label>
 <label class="chk"><input type="checkbox" required checked /><span>Согласен на обработку персональных данных</span></label>
 {btn("Отправить заявку", "btn--grad btn--block", 'type="submit"').replace(' type="button"', '')}
 <div class="ok" role="status"><img src="/img/3d/cross.webp" alt="" width="560" height="560" /><b>Заявка отправлена</b><span>Мы свяжемся с вами в ближайшее время</span></div>
</form></div></div>
<script type="module" src="/src/js/main.js"></script>'''

for n, c in (('head', HEAD), ('header', HEADER), ('footer', FOOTER)):
    open(f'{ROOT}/src/partials/{n}.html', 'w').write(c)

# ---------------- components ----------------
def page(fname, title, desc, body, extra_head=''):
    open(f'{ROOT}/{fname}', 'w').write(f'''<!doctype html>
<html lang="ru" class="no-js">
<head>
<!-- @include head -->
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}" />
<meta property="og:title" content="{E(title)}" />
<meta property="og:description" content="{E(desc)}" />
<meta property="og:image" content="/img/3d/dna.webp" />
{extra_head}
</head>
<body>
<!-- @include header -->
<main id="main">
{body}
</main>
<!-- @include footer -->
</body>
</html>
''')

def sec_head(kicker, title, right='', tag='h2'):
    return f'<div class="sec-head" data-reveal><div><span class="kicker">{kicker}</span><{tag} class="h2">{title}</{tag}></div>{right}</div>'

def dir_card(d, i=0):
    return f'''<article class="dir" style="--c:{d["c"]};--d:{(i%4)*0.06:.2f}s" data-reveal>
 <img class="dir__ic" src="/img/3d/{d["icon"]}.webp" alt="" width="560" height="560" loading="lazy" />
 <h3>{E(d["t"])}</h3><p>{E(d["d"])}</p>
 <div class="dir__f"><a class="link" href="/{"kardiologiya" if d["id"]=="kardiologiya" else "napravleniya#" + d["id"]}">Подробнее {I["arr"]}</a>{btn("Записаться", "btn--ink btn--plain", f'data-book="{E(d["t"].split(" ")[0])}"', "up").replace('<span class="btn__i">' + I["up"] + '</span>', '')}</div>
</article>'''

def dirs_grid(cta=True):
    cards = ''.join(dir_card(d, i) for i, d in enumerate(DIRS))
    c = f'''<div class="dir dir--cta" data-reveal><div><h3>Не нашли необходимую услугу?</h3><p>Оставьте заявку — мы свяжемся с вами, проконсультируем и подберём нужного специалиста.</p><div style="margin-top:20px">{btn("Оставить заявку", "btn--grad", "data-book")}</div></div><img src="/img/3d/dna.webp" alt="" width="560" height="560" loading="lazy" /></div>''' if cta else ''
    return f'<div class="dirs">{cards}{c}</div>'

def doc_card(d, i=0):
    return f'''<a class="doc" href="/vrachi#{d["d"]}" data-reveal style="--d:{(i%4)*0.06:.2f}s">
 <div class="doc__ph ph"><img src="{IMG(d["img"],620,780)}" alt="{E(d["n"])}" loading="lazy" /><span class="doc__xp">Стаж {d["xp"]}</span><span class="doc__go">{I["up"]}</span></div>
 <h3>{E(d["n"])}</h3><p>{E(d["r"])}</p><div class="tags">{"".join(f'<span class="tag">{E(t)}</span>' for t in d["tags"])}</div></a>'''

def check_card(c, i=0):
    old = f'<s>{c["old"]} сум</s>' if c['old'] else ''
    b = f'<span class="badge">{c["b"]}</span>' if c['b'] else ''
    hot = ' ck--hot' if c.get('hot') else ''
    cls = 'btn--grad' if c.get('hot') else 'btn--ink'
    return f'''<article class="ck{hot}" data-reveal style="--d:{(i%3)*0.06:.2f}s">
 <div class="ck__top"><div><div style="display:flex;gap:8px;align-items:center;margin-bottom:10px"><span class="tag">{c["n"]} исследований</span>{b}</div><h3>{E(c["t"])}</h3></div><img class="ck__ic" src="/img/3d/{c["icon"]}.webp" alt="" width="560" height="560" loading="lazy" /></div>
 <p class="sub">{E(c["s"])}</p>
 <ul>{"".join(f"<li>{E(x)}</li>" for x in c["items"])}</ul>
 <div class="tags"><span class="tag">Анализы</span><span class="tag">Диагностика</span><span class="tag">Консультация</span></div>
 <div class="ck__price"><div>{old}<b>{c["p"]} сум</b></div>{btn("Записаться", cls + " btn--sm", 'data-book="Чек-ап"')}</div>
</article>'''

def post_card(p, i=0):
    return f'''<a class="post" href="/statya" data-reveal style="--d:{(i%3)*0.06:.2f}s"><div class="post__ph ph"><img src="{IMG(p["img"],800,550)}" alt="" loading="lazy" /><span class="chip post__cat">{E(p["cat"])}</span></div><time>{p["date"]}</time><h3>{E(p["t"])}</h3><p>{E(p["d"])}</p></a>'''

def faq_block():
    items = ''.join(f'<details class="qa"{" open" if i==0 else ""}><summary>{E(q)}<i></i></summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(FAQ))
    return f'''<section class="sec"><div class="container faq">
 <div class="faq__side" data-reveal><span class="kicker">Вопрос-ответ</span><h2 class="h2">Частые вопросы</h2><p class="lead">Не нашли ответ? Задайте вопрос — ответим в течение рабочего дня.</p><div>{btn("Задать вопрос", "btn--ink", "data-book")}</div><img src="/img/3d/molecule.webp" alt="" width="560" height="560" loading="lazy" /></div>
 <div data-reveal style="--d:.08s">{items}</div></div></section>'''

MSG = f'''<section class="sec sec--top0"><div class="container"><div class="msg" data-reveal>
 <img class="msg__objs" src="/img/3d/drop.webp" alt="" width="560" height="560" loading="lazy" />
 <div><span class="kicker">Остались вопросы?</span><h2 class="h2" style="margin-top:14px">Напишите нам в любой мессенджер</h2><p class="lead" style="margin-top:12px">Ответим на все вопросы, поможем подготовиться к визиту и запишем к врачу.</p></div>
 <div class="msg__btns"><a class="mbtn" href="https://t.me/" target="_blank" rel="noopener"><span class="mbtn__ic" style="background:#2aabee">{I["tg"]}</span><div><span>Написать в</span><b>Telegram</b></div></a><a class="mbtn" href="https://wa.me/998712000000" target="_blank" rel="noopener"><span class="mbtn__ic" style="background:#25d366">{I["wa"]}</span><div><span>Написать в</span><b>WhatsApp</b></div></a></div>
</div></div></section>'''

BOOK = f'''<section class="sec sec--top0"><div class="container"><div class="book" data-reveal>
 <div class="book__copy"><div class="book__objs" aria-hidden="true"><img src="/img/3d/capsule.webp" alt="" width="560" height="560" loading="lazy"/><img src="/img/3d/heart.webp" alt="" width="560" height="560" loading="lazy"/><img src="/img/3d/molecule.webp" alt="" width="560" height="560" loading="lazy"/></div>
  <span class="kicker" style="color:#fff">Запись на приём</span><h2 class="h2">Запишитесь на приём к врачу</h2><p>Оставьте заявку — мы свяжемся с вами в ближайшее время и запишем на удобное время.</p></div>
 <form class="bform" data-form novalidate>
  <input class="" name="name" required placeholder="Ваше имя" autocomplete="name" aria-label="Ваше имя" />
  <input name="phone" type="tel" required placeholder="+998 __ ___-__-__" autocomplete="tel" inputmode="tel" aria-label="Телефон" />
  <select class="full" name="dir" aria-label="Направление"><option value="">Выберите направление</option>{opts}</select>
  <button class="btn btn--ink full" type="submit">Записаться на приём<span class="btn__i">{I["up"]}</span></button>
  <small class="full">Нажимая кнопку, вы соглашаетесь с обработкой персональных данных</small>
  <div class="ok" role="status"><img src="/img/3d/cross.webp" alt="" width="560" height="560" /><b>Заявка отправлена</b><span>Перезвоним в течение 15 минут</span></div>
 </form></div></div></section>'''

def phero(crumb, title, lead, art, extra='', dark=False):
    cls = ' phero--dark' if dark else ''
    a = art if art.startswith('<') else f'<img class="phero__art" src="/img/3d/{art}.webp" alt="" width="560" height="560" />'
    return f'''<section class="phero{cls}"><div class="container"><div class="phero__card{' dark' if dark else ''}">
 <div class="phero__copy"><nav class="crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a>{crumb}</nav><h1 class="display" style="font-size:clamp(32px,4.6vw,64px)" data-reveal>{title}</h1><p class="lead" data-reveal style="--d:.06s">{lead}</p>{extra}</div>
 {a}</div></div></section>'''

DIAG = f'''<section class="sec"><div class="diag dark" aria-labelledby="dg-t">
 <svg class="ecg-band" viewBox="0 0 1600 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60 H300 l20 -8 20 8 H420 l14 -50 18 80 16 -46 12 16 H760 l20 -8 20 8 H900 l14 -50 18 80 16 -46 12 16 H1240 l20 -8 20 8 H1380 l14 -50 18 80 16 -46 12 16 H1600"/></svg>
 <div class="container diag__grid">
  <div class="diag__copy">
   <span class="kicker">Диагностика</span>
   <h2 class="h2" id="dg-t">Точная диагностика <span class="grad-t">за один визит</span></h2>
   <p class="lead">Экспертное оборудование и собственная лаборатория: обследование, результаты и консультация врача — в одном месте и без очередей.</p>
   <div class="flist">
    <div class="fitem">{I["wave"]}<div><b>УЗИ экспертного класса</b><span>Все органы и сосуды, допплер</span></div></div>
    <div class="fitem">{I["ecg"]}<div><b>ЭКГ, Холтер, СМАД</b><span>Сердце под контролем 24 часа</span></div></div>
    <div class="fitem">{I["flask"]}<div><b>400+ анализов</b><span>Результаты онлайн от 2 часов</span></div></div>
    <div class="fitem">{I["scan"]}<div><b>ЭЭГ и УЗДГ</b><span>Нервная система и сосуды головы</span></div></div>
   </div>
   <div>{btn("Записаться на диагностику", "btn--grad", 'data-book="УЗИ"')}</div>
  </div>
  <div class="diag__stage">
   <div class="hud hud--a" aria-hidden="true"><div class="hud__h">Пульс <i></i></div><b><span data-bpm>72</span> уд/мин</b><svg class="ecg" viewBox="0 0 160 40"><path d="M0 24 H40 l6 -4 6 4 H70 l5 -18 7 30 6 -16 5 4 H120 l6 -4 6 4 H160"/></svg></div>
   <div class="hud hud--b" aria-hidden="true"><div class="hud__h">3D-сканирование</div><b data-scan-v>0%</b><div class="bar"><i data-scan-bar></i></div><span style="display:block;margin-top:8px">Ритм синусовый · норма</span></div>
   <div class="diag__canvas" data-heart3d></div>
   <div class="diag__fb"><img src="/img/3d/heart.webp" alt="" width="560" height="560" loading="lazy" /></div>
  </div>
 </div></div></section>'''

# ---------------- HOME ----------------
ABOUT_SEC = f'''<section class="sec"><div class="container about">
 <div class="collage" data-reveal>
  <div class="ph p1"><img src="{IMG("1759987383760-327efaf5522a",900,800)}" alt="Холл клиники INTERMED CENTER" loading="lazy" /></div>
  <div class="ph p2"><img src="{IMG("1758691461935-202e2ef6b69f",700,600)}" alt="Врач на приёме" loading="lazy" /></div>
  <img class="obj" src="/img/3d/cross.webp" alt="" width="560" height="560" loading="lazy" />
  <svg class="seal" viewBox="0 0 128 128" aria-hidden="true"><circle cx="64" cy="64" r="62" fill="#fff"/><g class="rot"><defs><path id="cp" d="M64 64 m-46 0 a46 46 0 1 1 92 0 a46 46 0 1 1 -92 0"/></defs><text><textPath href="#cp">здоровье · забота · точность · </textPath></text></g><circle cx="64" cy="64" r="24" fill="url(#sg)"/><defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#0fb3a6"/><stop offset="1" stop-color="#9b8cff"/></linearGradient></defs><path d="M64 54v20M54 64h20" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>
 </div>
 <div class="about__copy" data-reveal style="--d:.08s">
  <span class="kicker">О нас</span>
  <h2 class="h2">Клиника, где забота о здоровье — <span class="grad-t">главный приоритет</span></h2>
  <p class="t">INTERMED CENTER — многопрофильный медицинский центр, объединяющий опытных врачей разных специальностей, экспертную диагностику и собственную лабораторию.</p>
  <p class="t">Мы проводим комплексное обследование и лечение всего организма: УЗИ, ЭКГ, Холтер, кардиология, гинекология, урология, неврология, эндокринология и другие направления. Звоните и записывайтесь на приём уже сегодня!</p>
  <div class="values2"><div class="vcard"><img src="/img/3d/heart.webp" alt="" width="560" height="560" loading="lazy"/><b>Здоровье — наша главная ценность</b></div><div class="vcard"><img src="/img/3d/capsule.webp" alt="" width="560" height="560" loading="lazy"/><b>Внимательное отношение к каждому</b></div></div>
  <div>{btn("Подробнее о клинике", "btn--ink", "", "arr", "a", "/o-centre")}</div>
 </div>
</div></section>

<section class="sec sec--top0"><div class="container">
 {sec_head("Галерея", "Комфортные условия и дружелюбная атмосфера", '<div class="arrows" data-for="gal"><button data-prev aria-label="Назад">' + I["left"] + '</button><button data-next aria-label="Вперёд">' + I["right"] + '</button></div>')}
 <div class="strip" id="gal" data-strip>{"".join(f'<figure class="ph"><img src="{IMG(g,900,700)}" alt="{E(c)}" loading="lazy" draggable="false" /><figcaption>{E(c)}</figcaption></figure>' for g, c in GALLERY)}</div>
</div></section>

'''

avs = ''.join(f'<img src="{IMG(d["img"],90,90)}" alt="" loading="lazy" />' for d in DOCS[:3])
home = f'''
<section class="hero"><div class="container">
 <div class="hero__card">
  <div class="hero__copy">
   <span class="chip" data-reveal><span class="dot"></span>{ADDR.split(", ")[0]}, {ADDR.split(", ")[1]} · {HOURS.split(",")[0]}</span>
   <h1 class="display" data-reveal style="--d:.06s"><span class="l">Многопрофильная</span><span class="l">клиника <span class="grad-t">INTERMED</span></span><span class="l">CENTER</span></h1>
   <p class="lead" data-reveal style="--d:.12s">Команда ведущих врачей, экспертная диагностика и собственная лаборатория. Комплексные программы обследования всего организма — в одной клинике.</p>
   <div class="hero__ctas" data-reveal style="--d:.18s">{btn("Записаться на приём", "btn--grad", "data-book")}{btn("Пройти чек-ап", "btn--glass", "", "arr", "a", "/check-up")}</div>
   <div class="hero__minis" data-reveal style="--d:.24s">
    <div class="mini"><div class="avs">{avs}</div><div><b>20+</b><span>врачей-специалистов</span></div></div>
    <div class="mini"><span class="mini__ic"><img src="/img/3d/tube.webp" alt="" width="560" height="560" /></span><div><b>от 2 ч</b><span>результаты анализов онлайн</span></div></div>
   </div>
  </div>
  <div class="hero__stage">
   <div class="hero__canvas" data-hero3d></div>
   <div class="hero__fallback"><img src="/img/3d/dna.webp" alt="" width="560" height="560" /></div>
   <div class="fchip fchip--a"><span class="fchip__ic">{I["cal"]}</span><div><b>Онлайн-запись 24/7</b><span>Подтверждение за 15 минут</span></div></div>
   <div class="fchip fchip--b"><span class="fchip__ic">{I["shield"]}</span><div><b>Лицензия Минздрава</b><span>Республики Узбекистан</span></div></div>
  </div>
 </div>
 <div class="stats" data-reveal>
  <div><b data-count="20">20<sup>+</sup></b><span>специалистов</span></div>
  <div><b data-count="15">15<sup>+</sup></b><span>направлений</span></div>
  <div><b data-count="400">400<sup>+</sup></b><span>видов анализов</span></div>
  <div><b data-count="7000">7 000<sup>+</sup></b><span>пациентов в год</span></div>
 </div>
</div></section>

<section class="sec" id="napravleniya"><div class="container">
 {sec_head("Направления", "Широкий спектр <span class='grad-t'>медицинских услуг</span>", '<a class="link" href="/napravleniya">Все направления ' + I["arr"] + '</a>')}
 {dirs_grid()}
</div></section>

{DIAG}

{ABOUT_SEC}

<section class="sec sec--top0" style="padding-top:clamp(40px,5vw,72px)"><div class="container">
 {sec_head("Врачи", "Команда квалифицированных специалистов", '<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap"><a class="link" href="/vrachi">Все врачи ' + I["arr"] + '</a><div class="arrows" data-for="docs"><button data-prev aria-label="Назад">' + I["left"] + '</button><button data-next aria-label="Вперёд">' + I["right"] + '</button></div></div>')}
 <div class="docs" id="docs" data-strip>{"".join(doc_card(d, i) for i, d in enumerate(DOCS))}</div>
</div></section>

{BOOK}

<section class="sec sec--top0" style="padding-top:clamp(40px,5vw,72px)"><div class="container">
 {sec_head("Чек-апы", "Программы комплексного <span class='grad-t'>обследования организма</span>", '<a class="link" href="/check-up">Все чек-апы ' + I["arr"] + '</a>')}
 <div class="checks">{"".join(check_card(c, i) for i, c in enumerate(CHECKS))}</div>
</div></section>

<section class="sec sec--top0" style="padding-top:clamp(40px,5vw,72px)"><div class="container">
 {sec_head("Отзывы", "Отзывы о клинике INTERMED CENTER", '<p class="lead">Нам важно ваше мнение — читайте отзывы пациентов и делитесь своим опытом на картах.</p>')}
 <div class="plats" data-reveal>
  <a class="plat" href="https://maps.google.com/" target="_blank" rel="noopener"><span class="plat__logo" style="background:linear-gradient(135deg,#4285f4,#34a853)">G</span><div><b>Google Maps</b><span>Читать и оставить отзыв</span></div><span class="arr">{I["up"]}</span></a>
  <a class="plat" href="https://yandex.uz/maps/" target="_blank" rel="noopener"><span class="plat__logo" style="background:linear-gradient(135deg,#fc3f1d,#ff7a59)">Я</span><div><b>Яндекс Карты</b><span>Читать и оставить отзыв</span></div><span class="arr">{I["up"]}</span></a>
  <a class="plat" href="https://2gis.uz/tashkent" target="_blank" rel="noopener"><span class="plat__logo" style="background:linear-gradient(135deg,#19aa1e,#8bd437)">2</span><div><b>2ГИС</b><span>Читать и оставить отзыв</span></div><span class="arr">{I["up"]}</span></a>
 </div>
</div></section>

<section class="sec sec--top0" style="padding-top:clamp(40px,5vw,72px)"><div class="container">
 {sec_head("Блог", "Полезные статьи и новости", '<a class="link" href="/blog">Перейти в блог ' + I["arr"] + '</a>')}
 <div class="posts">{"".join(post_card(p, i) for i, p in enumerate(POSTS[:3]))}</div>
</div></section>

{faq_block()}
{MSG}
'''

CONTACTS = f'''<section class="sec" id="kontakty"><div class="container">
 {sec_head("Контакты", "Контактная информация")}
 <div class="contact">
  <div class="cinfo" data-reveal>
   <a class="ccard" href="tel:{TEL}"><span class="ccard__ic">{I["phone"]}</span><div><small>Телефон</small><b>{TEL_H}</b></div></a>
   <div class="ccard"><span class="ccard__ic">{I["pin"]}</span><div><small>Адрес</small><b>{ADDR}</b></div></div>
   <div class="ccard"><span class="ccard__ic">{I["clock"]}</span><div><small>Режим работы</small><b>{HOURS}</b></div></div>
   <a class="ccard" href="mailto:info@intermed.uz"><span class="ccard__ic">{I["mail"]}</span><div><small>E-mail</small><b>info@intermed.uz</b></div></a>
   <div class="req"><b>Реквизиты</b><span>ООО «INTERMED CENTER»</span><span>ИНН: — · Лицензия МЗ РУз: —</span></div>
  </div>
  <div class="map" data-reveal style="--d:.08s"><iframe title="Карта: INTERMED CENTER" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=69.315%2C41.330%2C69.355%2C41.350&amp;layer=mapnik&amp;marker=41.3405%2C69.3355"></iframe></div>
 </div>
</div></section>'''

page('index.html', 'INTERMED CENTER — многопрофильная клиника в Ташкенте', 'Многопрофильный медицинский центр INTERMED CENTER: терапия, кардиология, гинекология, урология, неврология, эндокринология, УЗИ и лаборатория. Чек-апы и запись онлайн.', home + CONTACTS, '<link rel="preload" href="/assets/heart.bin" as="fetch" crossorigin />')

# ---------------- DIRECTIONS ----------------
filters = '<button class="is-active" data-f="all">Все</button>' + ''.join(f'<button data-f="{d["id"]}">{E(d["t"].split(" и ")[0])}</button>' for d in DIRS)
srvs = ''
for d in DIRS:
    rows = ''.join(f'<div class="srv__row"><span>{E(n)}</span><b>{p} сум</b></div>' for n, p in d['srv'])
    more = f'<a class="link" href="/kardiologiya">Страница направления {I["arr"]}</a>' if d['id'] == 'kardiologiya' else ''
    srvs += f'''<article class="srv" id="{d["id"]}" data-cat="{d["id"]}" data-reveal><div class="srv__side"><img src="/img/3d/{d["icon"]}.webp" alt="" width="560" height="560" loading="lazy" /><h2>{E(d["t"])}</h2><p>{E(d["d"])}</p><div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">{btn("Записаться", "btn--grad btn--sm", f'data-book="{E(d["t"].split(" ")[0])}"')}{more}</div></div><div class="srv__list">{rows}</div></article>'''
page('napravleniya.html', 'Направления — INTERMED CENTER', 'Все направления многопрофильной клиники INTERMED CENTER и стоимость услуг.',
     phero('<span>Направления</span>', 'Направления <span class="grad-t">клиники</span>', 'Восемь ключевых направлений и более 400 видов исследований — диагностика, лечение и профилактика для всей семьи.', 'cross') +
     f'<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="container"><div class="chips-f" data-filter role="group" aria-label="Фильтр">{filters}</div>{srvs}<p class="note">Цены указаны в сумах и носят ознакомительный характер.</p></div></section>' + BOOK + faq_block())

# ---------------- CARDIOLOGY detail ----------------
d = DIRS[1]
treat = ['Гипертония и скачки давления','Аритмии и сердцебиение','Боли в груди и одышка','Ишемическая болезнь сердца','Повышенный холестерин','Реабилитация после инфаркта']
rows = ''.join(f'<div class="prow"><h3>{E(n)}</h3><b>{p} сум</b><button data-book="Кардиология" aria-label="Записаться">{I["arr"]}</button></div>' for n, p in d['srv'])
stage = '<div class="phero__stage"><div class="diag__canvas" data-heart3d style="position:absolute;inset:0"></div><div class="diag__fb"><img src="/img/3d/heart.webp" alt="" width="560" height="560" /></div></div>'
page('kardiologiya.html', 'Кардиология — INTERMED CENTER', 'Кардиолог в Ташкенте: ЭКГ, ЭхоКГ, Холтер, СМАД. Диагностика и лечение болезней сердца и сосудов.',
     phero('<a href="/napravleniya">Направления</a><span>Кардиология</span>', 'Кардиология', 'Диагностика, лечение и профилактика болезней сердца и сосудов. Точные методы обследования и эффективные схемы терапии.', stage, f'<div class="hero__ctas">{btn("Записаться к кардиологу", "btn--grad", "data-book=Кардиология")}</div>', dark=True) +
     f'''<section class="sec"><div class="container">{sec_head("С чем обращаются", "Что мы лечим")}<ul class="treat" data-reveal>{"".join(f"<li><i></i>{E(t)}</li>" for t in treat)}</ul></div></section>
<section class="sec sec--top0"><div class="container">{sec_head("Стоимость", "Услуги и цены")}<div class="pgroup" data-reveal><div class="pgroup__h"><img src="/img/3d/heart.webp" alt="" width="560" height="560"/><h2>Кардиология</h2></div>{rows}</div></div></section>
<section class="sec sec--top0"><div class="container">{sec_head("Специалист", "Ваш кардиолог")}<div class="docs docs--grid">{doc_card(DOCS[1])}</div></div></section>''' + BOOK + faq_block(), '<link rel="preload" href="/assets/heart.bin" as="fetch" crossorigin />')

# ---------------- DOCTORS ----------------
dfil = '<button class="is-active" data-f="all">Все</button>' + ''.join(f'<button data-f="{x["d"]}">{E(x["r"].split(" · ")[0])}</button>' for x in DOCS)
dcards = ''.join(doc_card(x, i).replace('<a class="doc"', f'<a id="{x["d"]}" data-cat="{x["d"]}" class="doc"').replace(f'href="/vrachi#{x["d"]}"', f'href="#" data-book="{E(x["r"].split(" ")[0][:6])}"') for i, x in enumerate(DOCS))
page('vrachi.html', 'Врачи — INTERMED CENTER', 'Врачи многопрофильной клиники INTERMED CENTER: терапевты, кардиологи, гинекологи, урологи, неврологи и эндокринологи.',
     phero('<span>Врачи</span>', 'Команда <span class="grad-t">специалистов</span>', 'Врачи высшей и первой категории с опытом от 9 лет. Нажмите на карточку, чтобы записаться к специалисту.', 'neuron') +
     f'<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="container"><div class="chips-f" data-filter role="group" aria-label="Фильтр">{dfil}</div><div class="docs docs--grid">{dcards}</div></div></section>' + BOOK)

# ---------------- CHECK-UPS ----------------
page('check-up.html', 'Чек-апы — INTERMED CENTER', 'Программы комплексного обследования организма: ежегодный чек-ап, кардиориск, мужское и женское здоровье, планирование беременности.',
     phero('<span>Чек-апы</span>', 'Чек-апы — <span class="grad-t">здоровье под контролем</span>', 'Готовые программы обследования: анализы, диагностика и консультация врача за 1–2 визита. Выгоднее, чем по отдельности.', 'dna') +
     f'''<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="container"><div class="checks">{"".join(check_card(c, i) for i, c in enumerate(CHECKS))}</div></div></section>
<section class="sec sec--top0"><div class="container">{sec_head("Как проходит чек-ап", "Три простых шага")}<div class="checks">
<article class="ck" data-reveal><img class="ck__ic" src="/img/3d/tube.webp" alt="" width="560" height="560"/><h3>1. Анализы утром</h3><p class="sub" style="margin:0">Сдаёте кровь натощак с 8:00 до 11:00 — без очередей.</p></article>
<article class="ck" data-reveal style="--d:.06s"><img class="ck__ic" src="/img/3d/drop.webp" alt="" width="560" height="560"/><h3>2. Диагностика</h3><p class="sub" style="margin:0">УЗИ, ЭКГ и другие исследования в тот же день.</p></article>
<article class="ck" data-reveal style="--d:.12s"><img class="ck__ic" src="/img/3d/cross.webp" alt="" width="560" height="560"/><h3>3. Заключение врача</h3><p class="sub" style="margin:0">Разбор результатов и персональные рекомендации.</p></article>
</div></div></section>''' + BOOK + faq_block())

# ---------------- PRICES ----------------
groups = ''.join(f'<div class="pgroup" id="p-{x["id"]}" data-reveal><div class="pgroup__h"><img src="/img/3d/{x["icon"]}.webp" alt="" width="560" height="560" loading="lazy"/><h2>{E(x["t"])}</h2></div>' + ''.join(f'<div class="prow"><h3>{E(n)}</h3><b>{p} сум</b><button data-book="{E(x["t"].split(" ")[0])}" aria-label="Записаться">{I["arr"]}</button></div>' for n, p in x['srv']) + '</div>' for x in DIRS)
page('ceny.html', 'Цены — INTERMED CENTER', 'Стоимость приёма врачей, анализов и диагностики в INTERMED CENTER.',
     phero('<span>Цены</span>', 'Цены на услуги', 'Прозрачная стоимость приёма, диагностики и анализов. Точный план и смету врач составит на консультации.', 'capsule') +
     f'<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="container">{groups}<p class="note">Цены указаны в сумах и носят ознакомительный характер. Не является публичной офертой.</p></div></section>' + BOOK)

# ---------------- ABOUT ----------------
docsl = ''.join(f'<a class="docl" href="#" data-reveal>{I["doc"]}<div><b>{E(t)}</b><span>{E(s)}</span></div></a>' for t, s in [('Лицензия МЗ РУз','PDF · медицинская деятельность'),('Свидетельство о регистрации','PDF · ООО «INTERMED CENTER»'),('Договор-оферта','PDF · условия оказания услуг'),('Политика персональных данных','PDF · обработка данных'),('Прейскурант','PDF · актуальные цены'),('Права и обязанности пациента','PDF · памятка')])
page('o-centre.html', 'О центре — INTERMED CENTER', 'О многопрофильном медицинском центре INTERMED CENTER: команда, оборудование, документы.',
     phero('<span>О центре</span>', 'О центре <span class="grad-t">INTERMED</span>', 'Многопрофильная клиника, где забота о вашем здоровье и благополучии — главный приоритет.', 'heart') +
     ABOUT_SEC + DIAG + f'<section class="sec"><div class="container">{sec_head("Документы", "Лицензии и документы")}<div class="docs-l">{docsl}</div></div></section>' + MSG)

# ---------------- BLOG ----------------
page('blog.html', 'Блог — INTERMED CENTER', 'Полезные статьи о здоровье от врачей INTERMED CENTER.',
     phero('<span>Блог</span>', 'Полезные статьи <span class="grad-t">и новости</span>', 'Врачи клиники рассказывают о профилактике, диагностике и здоровом образе жизни.', 'molecule') +
     f'<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="container"><div class="posts">{"".join(post_card(p, i) for i, p in enumerate(POSTS))}</div></div></section>' + MSG)

art = f'''<section class="sec" style="padding-top:clamp(32px,4vw,56px)"><div class="container"><article class="article">
<nav class="crumbs" aria-label="Хлебные крошки" style="margin-bottom:18px"><a href="/">Главная</a><a href="/blog" style="margin-left:0">/ Блог</a></nav>
<span class="chip">Профилактика · 12.10.2026 · 4 мин</span>
<h1 class="h2" style="margin:18px 0 28px">Симптомы, которые нельзя игнорировать</h1>
<div class="cover ph"><img src="{IMG(POSTS[0]["img"],1400,700)}" alt="" /></div>
<p>Многие откладывают визит к врачу, надеясь, что «само пройдёт». Но есть сигналы, при которых промедление может обойтись дорого. Разберём, на что стоит обратить внимание в первую очередь.</p>
<h2>Когда стоит записаться к врачу как можно скорее</h2>
<ul><li>Давящая боль или жжение в груди, особенно при нагрузке</li><li>Внезапная сильная головная боль, нарушение речи или зрения</li><li>Резкая потеря веса без видимой причины</li><li>Постоянная усталость, которая не проходит после отдыха</li><li>Изменения родинок, уплотнения, кровотечения</li></ul>
<div class="callout"><p><b>Важно:</b> при острой боли в груди, нарушении речи или слабости в руке и ноге немедленно вызывайте скорую помощь — 103.</p></div>
<h2>Почему важна профилактика</h2>
<p>Регулярный чек-ап помогает выявить заболевания на ранней стадии, когда лечение проще и эффективнее. Базовое обследование занимает всего пару часов, а результаты вы получите онлайн.</p>
<div style="margin-top:28px">{btn("Записаться на чек-ап", "btn--grad", 'data-book="Чек-ап"')}</div>
</article></div></section>
<section class="sec sec--top0"><div class="container">{sec_head("Читайте также", "Другие статьи")}<div class="posts">{"".join(post_card(p, i) for i, p in enumerate(POSTS[1:4]))}</div></div></section>'''
page('statya.html', 'Симптомы, которые нельзя игнорировать — блог INTERMED CENTER', 'Когда стоит не откладывать визит к врачу.', art)

# ---------------- CONTACTS ----------------
page('kontakty.html', 'Контакты — INTERMED CENTER', 'Адрес, телефон и режим работы клиники INTERMED CENTER в Ташкенте.',
     phero('<span>Контакты</span>', 'Контакты', 'Мы находимся в Мирзо-Улугбекском районе Ташкента. Есть парковка для пациентов.', 'drop') +
     CONTACTS.replace('<section class="sec" id="kontakty">', '<section class="sec" id="kontakty" style="padding-top:clamp(40px,5vw,64px)">') + BOOK + MSG +
     '<section class="sec sec--top0"><div class="container"><p class="note" id="privacy">Политика обработки персональных данных: данные, отправленные через формы сайта, используются только для записи на приём и не передаются третьим лицам.</p></div></section>')

# ---------------- 404 ----------------
page('404.html', 'Страница не найдена — INTERMED CENTER', 'Страница не найдена.',
     f'<section class="nf"><div class="nf__in"><div class="nf__code">4<img src="/img/3d/heart.webp" alt="" width="560" height="560"/>4</div><h1 class="h3">Такой страницы нет — но мы всегда на связи</h1><p class="lead" style="text-align:center">Вернитесь на главную или запишитесь на приём.</p><div class="hero__ctas" style="justify-content:center">{btn("На главную", "btn--ink", "", "arr", "a", "/")}{btn("Записаться", "btn--grad", "data-book")}</div></div></section>')

print('pages generated')
