"""ShahPremium rang tizimi — logotipdagi oltin mamont + iliq qora/fil suyagi fon.

Sahifalar hech qachon aniq rang nomini (indigo-7, grey-6, red-6 ...) ishlatmaydi,
faqat SEMANTIK nomlarni:

    Quasar ranglari:  primary / secondary / positive / negative / warning / info
                      (props("color=primary"), classes("text-negative") ...)
    Bizning klasslar: sp-text-2  — ikkinchi darajali matn
                      sp-muted   — izoh/yordamchi matn
                      sp-subtle  — eng xira matn ("ma'lumot yo'q" kabi)
                      sp-active  — tanlangan element foni (nav, chat ro'yxati)
                      sp-surface-2 — karta ichidagi ikkinchi daraja fon
                      sp-card    — asosiy karta

Har bir nomning YORUG' va QORONG'I mavzudagi qiymati quyida bitta joyda
belgilangan — shuning uchun ikkala mavzuda ham ranglar bir-biriga mos turadi.
"""

# ---- brend asosi (ikkala mavzuda ham bir xil) ----
INK = "#17140F"          # header / qora chrome
GOLD = "#B8912F"
GOLD_DEEP = "#8A6D1F"
GOLD_LIGHT = "#D4AF55"

# ---- YORUG' mavzu ----
LIGHT = {
    "bg": "#F7F4EC",
    "surface": "#FFFFFF",
    "surface-2": "#F3EDE0",
    "border": "#E4DBC6",
    "text": "#221E17",
    "text-2": "#564E40",
    "muted": "#766C5A",
    "subtle": "#958B76",
    "active-bg": "#F6ECD2",
    "active-text": GOLD_DEEP,
    "brand-text": GOLD_DEEP,
}
LIGHT_Q = {
    "primary": GOLD_DEEP,
    "secondary": GOLD,
    "accent": GOLD,
    "positive": "#3F7A4A",
    "negative": "#B23A2E",
    "warning": "#96600F",
    "info": "#3E6A86",
}

# ---- QORONG'I mavzu ----
DARK = {
    "bg": "#15130F",
    "surface": "#1F1B15",
    "surface-2": "#2A251D",
    "border": "#3A3327",
    "text": "#EDE7DA",
    "text-2": "#CFC6B3",
    "muted": "#A89F8C",
    "subtle": "#857C6A",
    "active-bg": "rgba(212,175,85,.14)",
    "active-text": GOLD_LIGHT,
    "brand-text": GOLD_LIGHT,
}
# Qorong'i fonda to'q ranglar xira ko'rinadi — shu sababli ochroq tovlanishlar.
DARK_Q = {
    "primary": GOLD_LIGHT,
    "secondary": "#C9A24A",
    "accent": "#C9A24A",
    "positive": "#7DBB84",
    "negative": "#E57A6C",
    "warning": "#E3AE55",
    "info": "#7FB0CF",
}


def apply_app_colors() -> None:
    """Quasar'ning standart ko'k palitrasini ilova darajasida almashtiradi
    (bir marta, ishga tushganda). Qorong'i mavzu qiymatlari CSS'da beriladi."""
    from nicegui import app

    app.colors(
        **LIGHT_Q,
        dark=DARK["surface"],
        dark_page=DARK["bg"],
    )


def _vars(tokens: dict[str, str]) -> str:
    return " ".join(f"--sp-{k}:{v};" for k, v in tokens.items())


def _qvars(tokens: dict[str, str]) -> str:
    # Quasar brend ranglarini body'ga INLINE style sifatida qo'yadi — ularni
    # qorong'i mavzuda almashtirish uchun !important shart.
    return " ".join(f"--q-{k}:{v} !important;" for k, v in tokens.items())


BRAND_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&display=swap" rel="stylesheet">'
)

_ON_COLOR = ", ".join(
    f"body.body--dark .bg-{name}" for name in ("primary", "secondary", "accent", "positive", "negative", "warning", "info")
)

BRAND_OVERRIDE_CSS = f"""
{BRAND_FONT_LINK}
<style>
  :root {{ {_vars(LIGHT)} }}
  body.body--dark {{ {_vars(DARK)} {_qvars(DARK_Q)} }}

  body {{ background:var(--sp-bg) !important; color:var(--sp-text); overflow-x:hidden; }}

  /* ---- brend ---- */
  .sp-brand {{ font-family:'Cinzel', 'Times New Roman', serif; letter-spacing:.06em; }}
  .sp-brand-text {{ color:var(--sp-brand-text); }}
  .q-header {{ border-bottom:1px solid rgba(212,175,85,.18); }}

  /* ---- semantik matn / fon klasslari ---- */
  .sp-text-2 {{ color:var(--sp-text-2) !important; }}
  .sp-muted {{ color:var(--sp-muted) !important; }}
  .sp-subtle {{ color:var(--sp-subtle) !important; }}
  .sp-active {{ background:var(--sp-active-bg) !important; color:var(--sp-active-text) !important; }}
  .sp-surface-2 {{ background:var(--sp-surface-2) !important; color:var(--sp-text); }}

  /* ---- yuzalar: karta, jadval, menyu, yon panel ---- */
  .q-card, .sp-card, .q-table__card, .q-menu, .q-drawer {{
    background:var(--sp-surface) !important; color:var(--sp-text);
  }}
  .sp-card {{ border-radius:14px; border:1px solid var(--sp-border); box-shadow:0 1px 3px rgba(23,20,15,.06); }}
  .q-drawer {{ border-color:var(--sp-border) !important; }}
  .q-separator {{ background:var(--sp-border) !important; }}
  .q-table th {{ color:var(--sp-muted); font-weight:600; }}
  .q-table th, .q-table td, .q-table thead tr, .q-table tbody td {{ border-color:var(--sp-border) !important; }}
  .q-table tbody tr:hover {{ background:var(--sp-surface-2); }}
  .q-expansion-item--expanded, .q-item {{ color:var(--sp-text); }}

  /* ---- forma maydonlari ---- */
  .q-field__label {{ color:var(--sp-muted); }}
  .q-field__native, .q-field__input, .q-field__prefix, .q-field__suffix {{ color:var(--sp-text); }}
  .q-field--outlined .q-field__control:before {{ border-color:var(--sp-border); }}
  .q-field--outlined:hover .q-field__control:before {{ border-color:var(--sp-muted); }}
  /* Chrome avtoto'ldirishi qorong'i fonda och-ko'k to'rtburchak chizardi. */
  input:-webkit-autofill, input:-webkit-autofill:hover, input:-webkit-autofill:focus {{
    -webkit-text-fill-color:var(--sp-text) !important;
    -webkit-box-shadow:0 0 0 1000px var(--sp-surface) inset !important;
    caret-color:var(--sp-text);
    transition:background-color 99999s;
  }}

  /* ---- tablar ---- */
  .q-tabs {{ color:var(--sp-muted); }}
  .q-tab--active {{ color:var(--q-primary); }}

  /* Qorong'i mavzuda to'ldirilgan rangli tugma/belgilar ochroq bo'ladi —
     ular ustidagi oq matn o'qilmay qolmasligi uchun qora matn. */
  {_ON_COLOR} {{ color:{INK} !important; }}

  /* ---- telefon moslashuvi ---- */
  .q-table__middle {{ overflow-x:auto; -webkit-overflow-scrolling:touch; }}
  @media (max-width: 599px) {{
    .q-table__middle {{ max-width:calc(100vw - 2rem); }}
    /* Dialoglar o'z `min-width:...px` qiymati bilan tor ekrandan chiqib ketmasin. */
    .q-dialog .q-card {{
      min-width:0 !important;
      width:92vw !important;
      max-width:92vw !important;
      max-height:88vh;
      overflow-y:auto;
    }}
  }}
</style>
"""
