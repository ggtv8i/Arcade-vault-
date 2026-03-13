╔════════════════════════════════════════════╗
║   🕹️  ARCADE VAULT v8 — دليل الاستخدام    ║
╚════════════════════════════════════════════╝

📁 البنية:
  index.html              ← الواجهة الرئيسية (HTML+CSS فقط)
  scan.py                 ← يولّد كل شيء
  start.bat               ← تشغيل السيرفر (Windows)
  start.sh                ← تشغيل السيرفر (Mac/Linux)
  systems/
    nes/
      index.html          ← قائمة ألعاب NES
      roms/               ← ضع هنا ملفات .nes
      bios/               ← (أنظمة BIOS فقط)
    gba/ snes/ psx/ ...   ← نفس البنية

══════════════════════════════════════════
🚀 طريقة الاستخدام:
══════════════════════════════════════════

1. ضع ملفات الروم في المجلد المناسب:
   مثال: systems/gba/roms/game.gba
   مثال: systems/nes/roms/mario.nes

2. للأنظمة التي تحتاج BIOS (PSX, Sega CD, Lynx):
   systems/psx/bios/scph1001.bin

3. شغّل الماسح:
   python scan.py
   (يولّد HTML لكل لعبة + يحدّث القوائم)

4. شغّل السيرفر:
   Windows: انقر مزدوج على start.bat
   Android: استخدم تطبيق "Simple HTTP Server"
   Mac/Linux: ./start.sh

5. افتح في المتصفح:
   http://localhost:8080/index.html

══════════════════════════════════════════
📱 على الهاتف (Android):
══════════════════════════════════════════
1. ضع مجلد Arcade Vault في ذاكرة الهاتف
2. افتح تطبيق Simple HTTP Server
3. حدّد مجلد Arcade Vault
4. شغّل السيرفر على port 8080
5. افتح في المتصفح: http://localhost:8080

══════════════════════════════════════════
🔌 Offline بدون إنترنت:
══════════════════════════════════════════
1. حمّل EmulatorJS من:
   https://github.com/EmulatorJS/EmulatorJS
2. ضع مجلد data/ بجانب index.html
3. في scan.py غيّر السطر:
   EJS_PATH = 'https://cdn.emulatorjs.org/latest/data/'
   إلى:
   EJS_PATH = '../../data/'
4. شغّل scan.py مجدداً

══════════════════════════════════════════
⚠️ ملاحظات:
══════════════════════════════════════════
• الواجهة الرئيسية والقوائم: HTML+CSS فقط ✅
• ملفات اللاعب: تستخدم JS لتشغيل EmulatorJS فقط
• يعمل على Android/iPhone/PC/Mac
• بعد كل إضافة لعبة: شغّل scan.py مجدداً

الإصدار: v8 · 25 نظام
