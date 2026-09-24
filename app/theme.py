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
    # Soyalar iliq-jigarrang tusda — sof qora soya fil suyagi fonda "iflos" ko'rinadi.
    "shadow-sm": "0 1px 2px rgba(60,45,15,.06), 0 1px 3px rgba(60,45,15,.05)",
    "shadow-md": "0 2px 4px rgba(60,45,15,.05), 0 10px 24px -8px rgba(60,45,15,.16)",
    "shadow-lg": "0 4px 8px rgba(60,45,15,.06), 0 18px 40px -12px rgba(60,45,15,.24)",
    "shadow-press": "inset 0 2px 4px rgba(60,45,15,.18)",
    "glow": "0 6px 18px -4px rgba(138,109,31,.45)",
    "scroll-thumb": "rgba(138,109,31,.35)",
    "scroll-thumb-hover": "rgba(138,109,31,.6)",
    "ring": "rgba(138,109,31,.22)",
    "bg-glow": "rgba(212,175,85,.12)",
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
    # Qorong'i fonda soya ko'rinmaydi — chuqurlik o'rniga yengil oltin "nur" beramiz.
    "shadow-sm": "0 1px 2px rgba(0,0,0,.4)",
    "shadow-md": "0 2px 4px rgba(0,0,0,.35), 0 10px 24px -8px rgba(0,0,0,.6)",
    "shadow-lg": "0 4px 8px rgba(0,0,0,.4), 0 18px 40px -12px rgba(0,0,0,.7)",
    "shadow-press": "inset 0 2px 5px rgba(0,0,0,.5)",
    "glow": "0 6px 20px -4px rgba(212,175,85,.4)",
    "scroll-thumb": "rgba(212,175,85,.28)",
    "scroll-thumb-hover": "rgba(212,175,85,.5)",
    "ring": "rgba(212,175,85,.25)",
    "bg-glow": "rgba(212,175,85,.06)",
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

  body {{
    background-color:var(--sp-bg) !important;
    background-image:radial-gradient(1100px 520px at 100% -10%, var(--sp-bg-glow), transparent 65%);
    background-attachment:fixed;
    color:var(--sp-text); overflow-x:hidden;
  }}

  /* ---- brend ---- */
  .sp-brand {{ font-family:'Cinzel', 'Times New Roman', serif; letter-spacing:.06em; }}
  .sp-brand-text {{ color:var(--sp-brand-text); }}
  .q-header {{ border-bottom:1px solid rgba(212,175,85,.18); }}
  /* Header ikkala mavzuda ham qora — ichidagi elementlar (til tanlagichi va h.k.)
     yorug' mavzuda ham qorong'i mavzu tokenlari bilan chizilsin. */
  .q-header {{
    --sp-text:{DARK["text"]}; --sp-muted:{DARK["muted"]}; --sp-surface:{DARK["surface"]};
    --sp-border:rgba(255,255,255,.22); color:{DARK["text"]};
  }}
  .q-header .q-field__native, .q-header .q-field__marginal {{ color:{DARK["text"]}; }}

  /* ---- yuzalar: karta, jadval, menyu, yon panel, vaqt/sana tanlagich ---- */
  .q-card, .sp-card, .q-table__card, .q-menu, .q-drawer, .q-date, .q-time, .q-uploader {{
    background-color:var(--sp-surface) !important; color:var(--sp-text);
  }}
  /* Quasar tab panelga o'z oq/qora fonini beradi — karta ichida alohida
     to'rtburchak bo'lib ko'rinardi. Fon ota-elementdan olinsin. */
  .q-tab-panels, .q-tab-panel {{ background:transparent !important; }}
  .q-tooltip {{ background:var(--sp-text); color:var(--sp-surface); border-radius:8px; font-size:12px; }}

  /* ---- semantik matn / fon klasslari (yuzalardan KEYIN — ularni bosib o'tishi uchun) ---- */
  .sp-text-2 {{ color:var(--sp-text-2) !important; }}
  .sp-muted {{ color:var(--sp-muted) !important; }}
  .sp-subtle {{ color:var(--sp-subtle) !important; }}
  .sp-surface-2 {{ background-color:var(--sp-surface-2) !important; color:var(--sp-text); }}
  .sp-active {{ background-color:var(--sp-active-bg) !important; color:var(--sp-active-text) !important; }}
  /* Kanban/navbat ustunlari: sahifa fonidan biroz ajralib turadigan "yo'lak",
     ichidagi oq/qora kartalar esa undan ko'tarilib ko'rinadi. */
  .sp-lane {{
    background-color:var(--sp-surface-2); color:var(--sp-text);
    border:1px solid var(--sp-border); border-radius:16px;
  }}

  /* ---- yumshoq konteynerlar: katta radius, qatlamli iliq soya, nozik yorug'lik ---- */
  .sp-card {{
    border-radius:16px; border:1px solid var(--sp-border);
    box-shadow:var(--sp-shadow-md);
    background-image:linear-gradient(180deg, rgba(255,255,255,.04), transparent 45%);
    transition:box-shadow .2s ease, border-color .2s ease, transform .18s ease;
  }}
  .q-card {{ border-radius:14px; }}
  .q-dialog .q-card {{ border-radius:18px; box-shadow:var(--sp-shadow-lg) !important; }}
  .q-dialog__backdrop {{ background:rgba(23,20,15,.38) !important; backdrop-filter:blur(3px); }}
  .q-menu {{ border-radius:12px; border:1px solid var(--sp-border); box-shadow:var(--sp-shadow-lg) !important; }}
  .q-table__card {{ border-radius:14px; border:1px solid var(--sp-border); box-shadow:var(--sp-shadow-sm) !important; overflow:hidden; }}
  .q-expansion-item.sp-card {{ overflow:hidden; }}
  .q-field--outlined .q-field__control {{ border-radius:10px; }}
  .q-badge {{ border-radius:999px; padding:3px 9px; }}
  .q-notification {{ border-radius:12px; box-shadow:var(--sp-shadow-lg); }}
  .q-header {{ box-shadow:var(--sp-shadow-sm); }}

  /* ---- tugmalar: ustiga kelganda ko'tariladi, bosilganda soya + halqa ---- */
  .q-btn {{ transition:transform .15s ease, box-shadow .2s ease, background-color .2s ease; }}
  .q-btn:not(.q-btn--round):not(.q-btn--rounded) {{ border-radius:10px; }}
  .q-btn:not(.q-btn--flat):not(.q-btn--outline) {{ box-shadow:var(--sp-shadow-sm); }}
  .q-btn:not(.q-btn--flat):not(.q-btn--outline):hover {{ box-shadow:var(--sp-glow); transform:translateY(-1px); }}
  .q-btn:not(.q-btn--flat):not(.q-btn--outline):active {{
    box-shadow:var(--sp-shadow-press), 0 0 0 4px var(--sp-ring);
    transform:translateY(0) scale(.98);
  }}
  .q-btn--flat:active, .q-btn--outline:active {{ box-shadow:0 0 0 4px var(--sp-ring); transform:scale(.96); }}

  /* ---- bosiladigan kartalar (boshqaruv panelidagi hisoblar) ---- */
  .sp-clickable {{ cursor:pointer; user-select:none; }}
  .sp-clickable:hover {{ transform:translateY(-3px); box-shadow:var(--sp-shadow-lg); border-color:rgba(212,175,85,.5); }}
  .sp-clickable:active {{
    transform:translateY(-1px) scale(.985);
    box-shadow:var(--sp-shadow-press), 0 0 0 4px var(--sp-ring);
  }}

  /* ---- yon panel navigatsiyasi ---- */
  .sp-nav-item {{ border-radius:10px; transition:background-color .15s ease, transform .12s ease; }}
  .sp-nav-item:not(.sp-active):hover {{ background:var(--sp-surface-2); }}
  .sp-nav-item:active {{ transform:scale(.98); }}
  /* Mini rejim: panel ekran chetida faqat ikonkalar bilan qoladi. */
  .q-drawer--mini.nicegui-drawer, .q-drawer--mini .nicegui-drawer {{ padding:8px !important; }}
  .q-drawer--mini .sp-nav-item {{ justify-content:center; padding-left:0 !important; padding-right:0 !important; }}
  .sp-nav-icon {{ font-size:20px; flex-shrink:0; }}

  /* Klaviatura bilan yurganda fokus ko'rinsin. */
  .q-btn:focus-visible, .sp-clickable:focus-visible, .sp-nav-item:focus-visible {{
    outline:2px solid var(--q-primary); outline-offset:2px;
  }}

  /* ---- scrollbar: ingichka, yumaloq, brend rangida ---- */
  ::-webkit-scrollbar {{ width:10px; height:10px; }}
  ::-webkit-scrollbar-track, ::-webkit-scrollbar-corner {{ background:transparent; }}
  ::-webkit-scrollbar-thumb {{
    background:var(--sp-scroll-thumb); border-radius:999px;
    border:3px solid transparent; background-clip:padding-box;
  }}
  ::-webkit-scrollbar-thumb:hover {{
    background:var(--sp-scroll-thumb-hover); border:2px solid transparent; background-clip:padding-box;
  }}
  /* Firefox ::-webkit-scrollbar'ni bilmaydi — unga standart xususiyatlar. */
  @supports not selector(::-webkit-scrollbar) {{
    * {{ scrollbar-width:thin; scrollbar-color:var(--sp-scroll-thumb) transparent; }}
  }}

  @media (prefers-reduced-motion: reduce) {{
    .q-btn, .sp-card, .sp-clickable, .sp-nav-item {{ transition:none !important; }}
    .q-btn:hover, .q-btn:active, .sp-clickable:hover, .sp-clickable:active {{ transform:none !important; }}
  }}
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
  /* MUHIM: NiceGUI 3 Quasar'ning !important klasslarini (.text-white va h.k.)
     `quasar_importants` CSS qatlamiga joylaydi. !important'da qatlamdagi qoida
     qatlamsiz qoidadan doim kuchli — shu sababli bunday qoidalar faqat undan
     OLDIN e'lon qilingan `overrides` qatlami ichida ishlaydi. */
  @layer overrides {{
    {_ON_COLOR} {{ color:{INK} !important; }}
  }}

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
