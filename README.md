# 🕹️ ARCADE VAULT — Cloud Gaming Platform

> **منصة ألعاب سحابية كاملة — ملف واحد يتحكم بكل شيء**

---

## 📁 هيكل المشروع

```
arcade-vault/
├── index.html          ← الموقع الكامل (لا تعدّل عليه)
├── games.json          ← ⭐ ملف الألعاب — هنا تضيف وتعدّل الألعاب
├── roms/               ← 📦 مجلد الألعاب — ضع ملفات الروم هنا
│   ├── sonic.md
│   ├── mario.nes
│   ├── zelda.gba
│   └── ...
├── .nojekyll
└── README.md
```

---

## ⚡ كيفية إضافة لعبة — 3 خطوات فقط

### الخطوة 1️⃣ — ضع ملف الروم في مجلد `roms/`

```
roms/
└── super-mario.nes     ← الملف هنا
```

### الخطوة 2️⃣ — أضف اللعبة في `games.json`

افتح ملف `games.json` وأضف كائن جديد في مصفوفة `games`:

```json
{
  "id": "mario-nes-001",
  "title": "Super Mario Bros",
  "system": "nes",
  "file": "super-mario.nes",
  "year": 1985,
  "genre": "Platform",
  "players": 1,
  "description": "أشهر لعبة نينتندو في التاريخ",
  "cover": "",
  "featured": true,
  "tags": []
}
```

### الخطوة 3️⃣ — ارفع التغييرات على GitHub

```bash
git add roms/super-mario.nes games.json
git commit -m "add: Super Mario Bros"
git push
```

**✅ اللعبة ستظهر فوراً في الموقع!**

---

## 🎮 الأنظمة المدعومة

| الكود | الاسم | الامتدادات |
|-------|-------|-----------|
| `nes` | Nintendo NES | `.nes` |
| `snes` | Super Nintendo | `.smc` `.sfc` `.zip` |
| `n64` | Nintendo 64 | `.n64` `.z64` `.v64` |
| `gba` | Game Boy Advance | `.gba` |
| `gb` | Game Boy | `.gb` |
| `gbc` | Game Boy Color | `.gbc` |
| `nds` | Nintendo DS | `.nds` |
| `md` | Sega Mega Drive | `.md` `.gen` `.bin` |
| `sms` | Sega Master System | `.sms` |
| `gg` | Sega Game Gear | `.gg` |
| `psx` | PlayStation 1 | `.bin` `.cue` `.pbp` |
| `psp` | PlayStation Portable | `.iso` `.cso` |
| `fbneo` | Arcade (FBNeo) | `.zip` |
| `mame` | Arcade (MAME) | `.zip` |
| `a2600` | Atari 2600 | `.a26` `.bin` |
| `dos` | MS-DOS | `.zip` `.exe` |

---

## ⚙️ إعدادات games.json

```json
"settings": {
  "site_title": "اسم موقعك",
  "site_subtitle": "وصف الموقع",
  "accent_color": "#8800ff",
  "emulatorjs_cdn": "https://cdn.emulatorjs.org/stable/data/",
  "roms_folder": "roms"
}
```

---

## 🌐 رفع على GitHub Pages

1. **New Repository** → `arcade-vault` → **Public**
2. ارفع الملفات (index.html + games.json + roms/)
3. **Settings** → **Pages** → **Deploy from branch: main** → **Save**
4. موقعك: `https://[username].github.io/arcade-vault/`

---

## 📝 مثال games.json كامل

```json
{
  "_info": { "version": "1.0" },
  "settings": {
    "site_title": "GAME VAULT",
    "site_subtitle": "مكتبتي الكلاسيكية",
    "accent_color": "#8800ff",
    "emulatorjs_cdn": "https://cdn.emulatorjs.org/stable/data/",
    "roms_folder": "roms"
  },
  "games": [
    {
      "id": "sonic-md-001",
      "title": "Sonic the Hedgehog",
      "system": "md",
      "file": "sonic.md",
      "year": 1991,
      "genre": "Platform",
      "players": 1,
      "description": "Sonic the Hedgehog — Sega Mega Drive",
      "cover": "",
      "featured": true,
      "tags": ["classic", "sega"]
    },
    {
      "id": "mario-gba-001",
      "title": "Super Mario Advance",
      "system": "gba",
      "file": "mario-advance.gba",
      "year": 2001,
      "genre": "Platform",
      "players": 1,
      "description": "Super Mario على GBA",
      "cover": "https://example.com/cover.jpg",
      "featured": false,
      "tags": ["nintendo", "mario"]
    }
  ]
}
```

---

## ⚖️ ملاحظة قانونية
هذه المنصة لا تتضمن أي ألعاب. أنت مسؤول عن امتلاك نسخ قانونية من الألعاب.

---
**ARCADE VAULT · Cloud Gaming Platform**
