"""ShahPremium brend palitrasi — logotipdagi oltin mamont + qora/neytral fonga
mos qilib, avvalgi keskin indigo o'rniga yumshoqroq, bir-biriga mos ranglar.
Har ikkala sahifa turi (shell() bilan o'ralganlar va login.py, o'ralmagan)
shu yerdan bitta manbadan foydalanadi.
"""

GOLD = "#B8912F"        # asosiy accent — ikonka/matn (och fonda yaxshi kontrast)
GOLD_DEEP = "#8A6D1F"   # tugma to'ldirilgan holati — oq matn bilan yetarli kontrast
GOLD_SOFT = "#FBF3DE"   # och krem fon — faol nav elementi, chip fon
INK = "#17140F"         # header/qora chrome
INK_2 = "#211D16"       # qorong'i rejimdagi karta foni
BODY_LIGHT = "#F7F4EC"  # yorug' rejim fon (iliq slonvoy)
BODY_DARK = "#15130F"   # qorong'i rejim fon


def apply_app_colors() -> None:
    """Quasar'ning STANDART primary rangini (ko'k, #5898d4) butun ilova
    darajasida oltin brendga almashtiradi.

    MUHIM: aynan shu — `color=indigo-7` kabi ANIQ ko'rsatilgan proplarni EMAS,
    balki hech qanday `color=` berilmagan barcha standart Quasar elementlari
    (ui.input fokus chizig'i, ui.switch, ui.tabs faol indikatori, checkbox,
    spinner) ko'k rangda qolib, oltin tugmalar bilan "to'qnashib" ko'rinishning
    asosiy sababi edi. Faqat bir marta, ilova ishga tushganda chaqiriladi
    (har sahifada emas — app darajasidagi sozlama).
    """
    from nicegui import app

    app.colors(
        primary=GOLD_DEEP,
        secondary=GOLD,
        accent=GOLD,
        dark=INK,
        dark_page=BODY_DARK,
    )

# Quasar'ning "indigo-*" statik utility klasslarini butun ilova bo'ylab
# qayta belgilaydi — 22 sahifadagi har bir alohida `color=indigo-7` chaqiruvini
# o'zgartirish o'rniga, bitta CSS bilan barcha joyda rang izchil almashadi.
BRAND_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&display=swap" rel="stylesheet">'
)

BRAND_OVERRIDE_CSS = f"""
{BRAND_FONT_LINK}
<style>
  .sp-brand {{ font-family:'Cinzel', 'Times New Roman', serif; letter-spacing:.06em; }}
  :root {{
    --sp-gold: {GOLD};
    --sp-gold-deep: {GOLD_DEEP};
    --sp-gold-soft: {GOLD_SOFT};
    --sp-ink: {INK};
  }}
  body {{ background:{BODY_LIGHT}; }}
  body.body--dark {{ background:{BODY_DARK}; color:#e9e4d8; }}
  body.body--dark .sp-card,
  body.body--dark .q-card {{ background:{INK_2}; color:#e9e4d8; }}
  body.body--dark .q-table {{ background:{INK_2}; color:#e9e4d8; }}
  .sp-card {{ border-radius:14px; }}

  /* indigo -> oltin (gold) — tugma to'ldirilgan holati */
  .bg-indigo-7, .bg-indigo-600, .bg-indigo-700 {{
    background:{GOLD_DEEP} !important; color:#fff !important;
  }}
  /* indigo matn/ikonka reng — och fonda o'qilishi uchun to'qroq tovlanish */
  .text-indigo-7, .text-indigo-700, .text-indigo-600 {{ color:{GOLD_DEEP} !important; }}
  .text-indigo-400, .text-indigo-4 {{ color:{GOLD} !important; }}
  /* indigo-50 fon (faol nav/chip) -> yumshoq krem-oltin tint */
  .bg-indigo-50 {{ background:{GOLD_SOFT} !important; }}
  body.body--dark .bg-indigo-50 {{ background:#2c2513 !important; }}
</style>
"""
