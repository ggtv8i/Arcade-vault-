#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arcade Vault v8 — ROM Scanner & Generator
==========================================
ضع ملفات الروم في systems/[id]/roms/
شغّل:  python scan.py
يولّد: ملف HTML لكل لعبة + قوائم HTML+CSS فقط

لا يحتاج سيرفر خاص — أي Simple HTTP Server يكفي
"""

import os, json, re, zipfile, shutil
from pathlib import Path

BASE    = Path(__file__).parent
SYSDIR  = BASE / 'systems'

# ── EmulatorJS path (غيّرها للـ offline) ──
EJS_PATH = 'https://cdn.emulatorjs.org/latest/data/'
# EJS_PATH = '../../data/'  # للاستخدام بدون إنترنت

# ══════════════════════════════════════════════
#  SYSTEMS TABLE
# ══════════════════════════════════════════════
SYSTEMS = [
    dict(id='nes',   name='NES',           full='Nintendo Entertainment System', core='nes',
         color='#e60012', bg='#1a0003',    ico='🎮', year=1983,
         exts=['.nes'], bios=[]),
    dict(id='snes',  name='SNES',          full='Super Nintendo',                core='snes',
         color='#7B2FBE', bg='#0d0118',    ico='🎮', year=1990,
         exts=['.smc','.sfc'], bios=[]),
    dict(id='n64',   name='N64',           full='Nintendo 64',                   core='n64',
         color='#009ac7', bg='#00101a',    ico='🎮', year=1996,
         exts=['.n64','.z64','.v64'], bios=[]),
    dict(id='gb',    name='Game Boy',      full='Nintendo Game Boy',             core='gb',
         color='#8BAC0F', bg='#0d1200',    ico='🕹️', year=1989,
         exts=['.gb'], bios=[]),
    dict(id='gbc',   name='GBC',           full='Game Boy Color',                core='gbc',
         color='#00bfff', bg='#001520',    ico='🕹️', year=1998,
         exts=['.gbc'], bios=[]),
    dict(id='gba',   name='GBA',           full='Game Boy Advance',              core='gba',
         color='#9B59B6', bg='#0e0018',    ico='🕹️', year=2001,
         exts=['.gba'], bios=[]),
    dict(id='nds',   name='NDS',           full='Nintendo DS',                   core='nds',
         color='#e52421', bg='#1a0000',    ico='🎮', year=2004,
         exts=['.nds'], bios=[]),
    dict(id='gc',    name='GameCube',      full='Nintendo GameCube',             core='dolphin',
         color='#6a0dad', bg='#0a0012',    ico='🎲', year=2001,
         exts=['.iso','.gcm','.gcz'], bios=[]),
    dict(id='md',    name='Mega Drive',    full='Sega Mega Drive / Genesis',     core='segaMD',
         color='#0057a8', bg='#000a14',    ico='🕹️', year=1988,
         exts=['.md','.gen','.smd','.bin'], bios=[]),
    dict(id='sms',   name='Master Sys',   full='Sega Master System',            core='segaMS',
         color='#1a6b9a', bg='#000d14',    ico='🕹️', year=1985,
         exts=['.sms'], bios=[]),
    dict(id='gg',    name='Game Gear',    full='Sega Game Gear',                core='segaGG',
         color='#0a9060', bg='#000f0a',    ico='🕹️', year=1990,
         exts=['.gg'], bios=[]),
    dict(id='scd',   name='Sega CD',      full='Sega CD / Mega-CD',             core='segaCD',
         color='#1a8a3c', bg='#000f06',    ico='💿', year=1991,
         exts=['.bin','.cue','.iso','.chd'],
         bios=['bios_CD_U.bin','bios_CD_E.bin','bios_CD_J.bin']),
    dict(id='s32x',  name='Sega 32X',     full='Sega 32X',                      core='sega32x',
         color='#c0392b', bg='#180200',    ico='🕹️', year=1994,
         exts=['.32x','.bin'], bios=[]),
    dict(id='psx',   name='PlayStation',  full='PlayStation 1',                 core='psx',
         color='#003791', bg='#000513',    ico='🎮', year=1994,
         exts=['.bin','.cue','.img','.pbp','.chd'],
         bios=['scph1001.bin','scph5501.bin','scph7001.bin']),
    dict(id='psp',   name='PSP',          full='PlayStation Portable',          core='ppsspp',
         color='#003087', bg='#000410',    ico='🎮', year=2005,
         exts=['.iso','.cso','.pbp'], bios=[]),
    dict(id='fbneo', name='FBNeo',        full='Final Burn Neo (Arcade)',       core='fbneo',
         color='#e6a800', bg='#141000',    ico='🕹️', year=1990,
         exts=['.zip'], bios=[]),
    dict(id='mame',  name='MAME',         full='MAME 2003 Plus',                core='mame2003plus',
         color='#ff4444', bg='#180000',    ico='🕹️', year=1997,
         exts=['.zip'], bios=[]),
    dict(id='a2600', name='Atari 2600',   full='Atari 2600 VCS',                core='atari2600',
         color='#ff6600', bg='#180800',    ico='🕹️', year=1977,
         exts=['.a26','.bin','.rom'], bios=[]),
    dict(id='a7800', name='Atari 7800',   full='Atari 7800 ProSystem',          core='atari7800',
         color='#cc4400', bg='#140500',    ico='🕹️', year=1984,
         exts=['.a78','.bin'], bios=[]),
    dict(id='lynx',  name='Atari Lynx',   full='Atari Lynx',                    core='lynx',
         color='#ff8c00', bg='#150900',    ico='🕹️', year=1989,
         exts=['.lnx'], bios=['lynxboot.img']),
    dict(id='pce',   name='PC Engine',    full='PC Engine / TurboGrafx-16',     core='pce',
         color='#ff6b35', bg='#160800',    ico='🕹️', year=1987,
         exts=['.pce'], bios=[]),
    dict(id='ngp',   name='Neo Geo P',    full='Neo Geo Pocket',                core='ngp',
         color='#4A0E8F', bg='#080010',    ico='🕹️', year=1998,
         exts=['.ngp'], bios=[]),
    dict(id='ws',    name='WonderSwan',   full='WonderSwan',                    core='ws',
         color='#0099cc', bg='#001014',    ico='🕹️', year=1999,
         exts=['.ws'], bios=[]),
    dict(id='wsc',   name='WSwan Color',  full='WonderSwan Color',              core='wsc',
         color='#ff66aa', bg='#180010',    ico='🕹️', year=2000,
         exts=['.wsc'], bios=[]),
    dict(id='dos',   name='DOS',          full='MS-DOS',                        core='dosbox',
         color='#00cc55', bg='#001208',    ico='💻', year=1981,
         exts=['.zip','.exe'], bios=[]),
]

SYS_BY_ID = {s['id']: s for s in SYSTEMS}

# ══════════════════════════════════════════════
#  CSS SHARED STYLES
# ══════════════════════════════════════════════
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Chakra+Petch:wght@400;600;700&display=swap');
:root{
  --bg:#07071c;--tx:#c8ceff;--mt:#3a3a60;--ht:#1a1a38;
  --fd:'Share Tech Mono','Courier New',monospace;
  --fb:'Chakra Petch',system-ui,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:rgba(0,0,0,0)}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--tx);font-family:var(--fb);min-height:100dvh;
  -webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img{display:block}

/* scanline overlay */
body::after{content:'';position:fixed;inset:0;z-index:9999;pointer-events:none;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.03) 2px,rgba(0,0,0,.03) 4px);
  animation:scan 8s linear infinite}
@keyframes scan{from{background-position:0 0}to{background-position:0 32px}}

/* grid noise */
body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    radial-gradient(ellipse 60% 40% at 15% 20%,rgba(136,0,255,.06),transparent 60%),
    radial-gradient(ellipse 50% 50% at 85% 80%,rgba(0,100,255,.04),transparent 60%);
  }

/* ── top bar ── */
.topbar{position:sticky;top:0;z-index:100;
  background:rgba(7,7,28,.9);backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,.06);padding:0 16px}
.tb-inner{max-width:900px;margin:0 auto;height:54px;
  display:flex;align-items:center;gap:12px}
.logo-wrap{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-box{width:32px;height:32px;border-radius:8px;
  background:linear-gradient(135deg,#8800ff,#ff0088);
  display:grid;place-items:center;font-size:16px;
  box-shadow:0 0 16px rgba(136,0,255,.35)}
.logo-name{font-family:var(--fd);font-size:12px;font-weight:700;letter-spacing:3px;
  background:linear-gradient(90deg,#bb66ff,#ff66bb,#66ffcc);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.tb-mid{flex:1;display:flex;justify-content:center}
.breadcrumb{font-family:var(--fd);font-size:9px;letter-spacing:2px;color:var(--mt);
  display:flex;align-items:center;gap:6px}
.breadcrumb a{color:var(--mt);transition:color .15s}
.breadcrumb a:hover{color:#bb66ff}
.breadcrumb span{color:var(--tx)}
.tb-right{display:flex;align-items:center;gap:6px;font-family:var(--fd);font-size:8px;color:var(--mt);letter-spacing:1.5px}
.tb-dot{width:5px;height:5px;border-radius:50%;background:#00cc55;
  box-shadow:0 0 6px #00cc55;animation:pulse 2s ease infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

/* ── section header ── */
.sec-head{max-width:900px;margin:0 auto;padding:28px 16px 16px}
.sec-tag{font-family:var(--fd);font-size:8px;letter-spacing:3px;color:var(--mt);
  display:flex;align-items:center;gap:8px;margin-bottom:8px}
.sec-tag::before{content:'';width:18px;height:1px;background:var(--mt)}
.sec-title{font-size:clamp(18px,5vw,32px);font-weight:700;color:#fff;line-height:1;
  display:flex;align-items:center;gap:10px}
.sec-sub{font-size:12px;color:var(--mt);margin-top:5px;font-family:var(--fd)}

/* ── system grid ── */
.sys-grid{max-width:900px;margin:0 auto;padding:0 12px 20px;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px}
@media(max-width:360px){.sys-grid{grid-template-columns:repeat(2,1fr)}}

.sys-card{--c:#8800ff;--bg2:#07071c;position:relative;border-radius:12px;overflow:hidden;
  display:block;background:var(--bg2);border:1px solid rgba(255,255,255,.05);
  transition:transform .22s,box-shadow .22s,border-color .22s;
  padding:14px 12px 12px;cursor:pointer}
.sys-card::before{content:'';position:absolute;top:0;inset-inline:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--c),transparent)}
.sys-card:hover{transform:translateY(-5px);border-color:var(--c);
  box-shadow:0 14px 36px rgba(0,0,0,.5),0 0 20px color-mix(in srgb,var(--c) 22%,transparent)}
.sys-card:active{transform:scale(.95)}
.sys-ico{font-size:24px;margin-bottom:8px;display:block;
  transition:transform .22s;transform-origin:left center}
.sys-card:hover .sys-ico{transform:scale(1.15) rotate(-5deg)}
.sys-name{font-family:var(--fd);font-size:10px;font-weight:700;color:#fff;
  letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sys-full{font-size:9px;color:var(--mt);white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;margin-top:2px;line-height:1.3}
.sys-foot{display:flex;justify-content:space-between;align-items:center;margin-top:10px}
.sys-year{font-family:var(--fd);font-size:8px;color:var(--ht,#1a1a38)}
.sys-count{font-family:var(--fd);font-size:8px;padding:2px 7px;border-radius:5px;
  background:rgba(255,255,255,.04);color:var(--mt);transition:all .15s}
.sys-count.has{background:color-mix(in srgb,var(--c) 18%,transparent);
  color:var(--c);border:1px solid color-mix(in srgb,var(--c) 35%,transparent)}
.sys-badge{position:absolute;top:6px;right:6px;font-family:var(--fd);font-size:7px;
  padding:1px 5px;border-radius:3px;letter-spacing:.5px}
.sys-badge.bios{background:rgba(255,200,0,.1);border:1px solid rgba(255,200,0,.25);color:#ffcc66}

/* ── games list ── */
.games-grid{max-width:900px;margin:0 auto;padding:0 12px 80px;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px}
@media(max-width:360px){.games-grid{grid-template-columns:repeat(2,1fr)}}

.game-card{--c:#8800ff;position:relative;display:block;border-radius:10px;
  background:linear-gradient(160deg,var(--gbg,#0d0020),#07071c);
  border:1px solid rgba(255,255,255,.05);transition:transform .22s,border-color .22s,box-shadow .22s;
  overflow:hidden}
.game-card::after{content:'';position:absolute;inset:0;
  background:linear-gradient(160deg,color-mix(in srgb,var(--c) 5%,transparent),transparent 60%);
  pointer-events:none;transition:opacity .22s;opacity:0}
.game-card:hover{transform:translateY(-5px) scale(1.02);border-color:var(--c);
  box-shadow:0 16px 38px rgba(0,0,0,.5),0 0 22px color-mix(in srgb,var(--c) 20%,transparent)}
.game-card:hover::after{opacity:1}
.game-card:active{transform:scale(.95)}
.game-art{width:100%;aspect-ratio:3/4;display:flex;align-items:center;justify-content:center;
  font-size:42px;position:relative;overflow:hidden}
.game-art-bg{position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 40%,color-mix(in srgb,var(--c) 18%,transparent),transparent 70%)}
.game-art-ico{position:relative;z-index:1;font-size:44px;
  filter:drop-shadow(0 0 16px var(--c));
  transition:transform .25s}
.game-card:hover .game-art-ico{transform:scale(1.12) rotate(-4deg)}
.game-art-sys{position:absolute;bottom:5px;right:5px;font-family:var(--fd);font-size:7px;
  padding:2px 6px;border-radius:4px;letter-spacing:.5px;
  background:color-mix(in srgb,var(--c) 20%,rgba(0,0,0,.7));
  color:var(--c);border:1px solid color-mix(in srgb,var(--c) 35%,transparent)}
.game-info{padding:8px 9px 10px}
.game-name{font-size:11px;font-weight:700;color:#fff;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  margin-bottom:3px;line-height:1.2}
.game-meta{display:flex;justify-content:space-between;align-items:center}
.game-ext{font-family:var(--fd);font-size:8px;color:var(--mt)}
.game-sz{font-size:9px;color:var(--mt)}
.game-play{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:center;
  padding-bottom:10px;opacity:0;transition:opacity .18s}
.game-card:hover .game-play{opacity:1}
.play-btn{background:var(--c);color:#fff;font-family:var(--fd);font-size:10px;
  font-weight:700;letter-spacing:2px;padding:7px 22px;border-radius:7px;
  box-shadow:0 4px 18px color-mix(in srgb,var(--c) 40%,transparent);
  white-space:nowrap}

/* ── empty state ── */
.empty-box{max-width:900px;margin:40px auto;padding:40px 20px;text-align:center}
.empty-ico{font-size:48px;display:block;margin-bottom:12px;opacity:.25}
.empty-title{font-family:var(--fd);font-size:13px;color:#fff;margin-bottom:6px;letter-spacing:1px}
.empty-txt{font-size:11px;color:var(--mt);line-height:1.7;max-width:260px;margin:0 auto}
.empty-cmd{margin-top:14px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  border-radius:8px;padding:10px 16px;display:inline-block;
  font-family:var(--fd);font-size:11px;color:#00cc55;letter-spacing:.5px}

/* ── player page ── */
#emu-shell{position:fixed;inset:0;display:flex;flex-direction:column;background:#000}
.emu-bar{height:42px;flex-shrink:0;background:rgba(5,5,20,.97);
  border-bottom:1px solid rgba(255,255,255,.06);
  display:flex;align-items:center;padding:0 10px;gap:7px;z-index:10}
.emu-back{width:32px;height:32px;border-radius:7px;background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.07);color:#fff;font-size:20px;
  display:grid;place-items:center;flex-shrink:0;text-decoration:none;
  transition:background .15s}
.emu-back:hover{background:rgba(255,255,255,.15)}
.emu-info{flex:1;min-width:0;text-align:center}
.emu-name{font-family:var(--fd);font-size:11px;font-weight:700;color:#fff;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.emu-sys{font-size:8px;color:#2a2a50;letter-spacing:1.5px;font-family:var(--fd)}
.emu-fs{width:32px;height:32px;border-radius:7px;background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.07);color:#fff;font-size:14px;
  display:grid;place-items:center;flex-shrink:0;cursor:pointer;
  transition:background .15s;-webkit-appearance:none;appearance:none}
.emu-fs:hover{background:rgba(255,255,255,.15)}
#emu-game{flex:1;border:none;background:#000}

/* ── footer ── */
.footer{border-top:1px solid var(--ht);padding:20px 16px;text-align:center;
  font-family:var(--fd);font-size:8px;color:var(--mt);letter-spacing:2px;margin-top:10px}

/* ── scroll ── */
::-webkit-scrollbar{width:2px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--ht);border-radius:2px}
"""

# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def slug(name):
    """Convert game name to safe filename"""
    n = re.sub(r'[^\w\s-]', '', name)
    n = re.sub(r'[\s_]+', '_', n.strip())
    return n[:60] or 'game'

def fmtsize(b):
    if b < 1024:      return f'{b}B'
    if b < 1048576:   return f'{b//1024}KB'
    return f'{b/1048576:.1f}MB'

def find_bios(sys_dir, bios_names):
    """Find first available bios file"""
    bios_dir = sys_dir / 'bios'
    for bn in bios_names:
        p = bios_dir / bn
        if p.exists():
            return f'bios/{bn}'
    return ''

# ══════════════════════════════════════════════
#  PLAYER.HTML — per game, uses EmulatorJS
# ══════════════════════════════════════════════
def make_player(rom_name, rom_file, sys, bios_path='', depth=2):
    back_path = '../' * depth + 'systems/' + sys['id'] + '/index.html'
    dots = '../' * depth

    bios_banner = ''
    if sys['bios'] and not bios_path:
        bios_banner = f'''
    <div style="position:absolute;top:50px;inset-inline:0;z-index:5;padding:8px 12px;
      background:rgba(255,180,0,.1);border-bottom:1px solid rgba(255,180,0,.2);
      font-family:'Share Tech Mono',monospace;font-size:10px;color:#ffcc66;text-align:center">
      ⚠️ لم يُعثر على ملف BIOS · ضع {', '.join(sys['bios'])} في systems/{sys['id']}/bios/ ثم شغّل scan.py
    </div>'''

    heavy = sys['id'] in ('gc','psp','n64')
    heavy_banner = ''
    if heavy:
        heavy_banner = '''
    <div style="position:absolute;top:50px;inset-inline:0;z-index:5;padding:6px 12px;
      background:rgba(255,100,0,.08);border-bottom:1px solid rgba(255,100,0,.2);
      font-family:'Share Tech Mono',monospace;font-size:10px;color:#ff8844;text-align:center">
      ⚡ هذا النظام ثقيل — يحتاج متصفح حديث وجهاز قوي
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>{rom_name} — {sys['name']}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:#000}}
#emu-shell{{position:fixed;inset:0;display:flex;flex-direction:column}}
.emu-bar{{height:42px;flex-shrink:0;background:rgba(5,5,20,.98);
  border-bottom:1px solid rgba(255,255,255,.06);
  display:flex;align-items:center;padding:0 10px;gap:7px}}
.emu-back{{width:32px;height:32px;border-radius:7px;background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.07);color:#fff;font-size:20px;
  display:grid;place-items:center;text-decoration:none;transition:background .15s}}
.emu-back:hover{{background:rgba(255,255,255,.15)}}
.emu-info{{flex:1;min-width:0;text-align:center}}
.emu-name{{font-family:'Share Tech Mono','Courier New',monospace;font-size:11px;
  font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.emu-sys{{font-size:8px;color:#2a2a50;letter-spacing:1.5px;
  font-family:'Share Tech Mono','Courier New',monospace}}
.emu-fs{{width:32px;height:32px;border-radius:7px;background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.07);color:#fff;font-size:14px;
  display:grid;place-items:center;flex-shrink:0;cursor:pointer;
  transition:background .15s;border:none}}
.emu-fs:hover{{background:rgba(255,255,255,.15)}}
#g{{flex:1;border:none;background:#000;position:relative}}
#ef{{width:100%;height:100%;border:none}}
</style>
</head>
<body>
<div id="emu-shell">
  <div class="emu-bar">
    <a class="emu-back" href="{back_path}">‹</a>
    <div class="emu-info">
      <div class="emu-name">{rom_name}</div>
      <div class="emu-sys">{sys['name'].upper()} · {sys['full'].upper()}</div>
    </div>
    <button class="emu-fs" onclick="(document.fullscreenElement?document.exitFullscreen():document.getElementById('g').requestFullscreen?.())">⛶</button>
  </div>
  <div id="g" style="position:relative">
    {bios_banner}
    {heavy_banner}
    <iframe id="ef" allowfullscreen allow="autoplay;fullscreen;gamepad"></iframe>
  </div>
</div>
<script>
(function(){{
  var ejs='{EJS_PATH}';
  var bios='{bios_path}';
  var romPath='{dots}{rom_file}';
  var html='<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#000;overflow:hidden}}#e{{width:100%;height:100%}}</style></head><body><div id="e"></div><script>'
    +'window.EJS_player="#e";'
    +'window.EJS_gameName={json.dumps(rom_name)};'
    +'window.EJS_gameUrl="'+romPath+'";'
    +'window.EJS_core="{sys["core"]}";'
    +'window.EJS_pathtodata="'+ejs+'";'
    +'window.EJS_biosUrl="'+bios+'";'
    +'window.EJS_startOnLoaded=true;'
    +'window.EJS_color="{sys["color"]}";'
    +'window.EJS_backgroundColor="#000000";'
    +'window.EJS_defaultOptions={{"save-state-slot":"1","save-state-location":"keep in browser"}};'
    +'window.EJS_Buttons={{playPause:true,restart:true,mute:true,settings:true,fullscreen:true,saveState:true,loadState:true,gamepad:true,volume:true,saveSavFiles:true,loadSavFiles:true,screenshot:true}};'
    +'var s=document.createElement("script");s.src="'+ejs+'loader.js";document.body.appendChild(s);'
    +'<\\/script></body></html>';
  document.getElementById('ef').srcdoc=html;
}})();
</script>
</body>
</html>
'''

# ══════════════════════════════════════════════
#  SYSTEM INDEX.HTML — game list, HTML+CSS only
# ══════════════════════════════════════════════
def make_sys_index(sys, games):
    col   = sys['color']
    bg2   = sys['bg']
    icon  = sys['ico']

    # build game cards
    cards_html = ''
    for g in games:
        sz = fmtsize(g['size'])
        ext = g['ext'].lstrip('.').upper()
        cards_html += f'''
    <a class="game-card" href="{g['slug']}.html"
       style="--c:{col};--gbg:{bg2}">
      <div class="game-art">
        <div class="game-art-bg"></div>
        <div class="game-art-ico">{icon}</div>
        <div class="game-art-sys">{sys["name"]}</div>
      </div>
      <div class="game-info">
        <div class="game-name">{g["name"]}</div>
        <div class="game-meta">
          <span class="game-ext">{ext}</span>
          <span class="game-sz">{sz}</span>
        </div>
      </div>
      <div class="game-play"><div class="play-btn">▶ PLAY</div></div>
    </a>'''

    empty_html = ''
    if not games:
        empty_html = f'''
  <div class="empty-box">
    <span class="empty-ico">{icon}</span>
    <div class="empty-title">لا توجد ألعاب</div>
    <div class="empty-txt">ضع ملفات الروم في<br>systems/{sys["id"]}/roms/<br>ثم شغّل scan.py</div>
    <div class="empty-cmd">python scan.py</div>
  </div>'''

    bios_note = ''
    if sys['bios']:
        bios_note = f'<span style="color:#ffcc66">· BIOS: {", ".join(sys["bios"])}</span>'

    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>{sys["name"]} · Arcade Vault</title>
<style>
{BASE_CSS}
</style>
</head>
<body>
<!-- TOP BAR -->
<div class="topbar">
  <div class="tb-inner">
    <div class="logo-wrap">
      <div class="logo-box">🕹️</div>
      <div class="logo-name">ARCADE VAULT</div>
    </div>
    <div class="tb-mid">
      <div class="breadcrumb">
        <a href="../../index.html">HOME</a>
        <span>›</span>
        <span>{sys["name"].upper()}</span>
      </div>
    </div>
    <div class="tb-right">
      <div class="tb-dot"></div>
      <span>LOCAL</span>
    </div>
  </div>
</div>

<!-- HEADER -->
<div class="sec-head">
  <div class="sec-tag">{sys["ico"]} {sys["year"]} {bios_note}</div>
  <div class="sec-title" style="color:{col}">{sys["full"]}</div>
  <div class="sec-sub">{len(games)} {'لعبة' if games else 'ألعاب'} · {sys["name"]}</div>
</div>

<!-- GAMES -->
{f'<div class="games-grid">{cards_html}</div>' if games else empty_html}

<div class="footer">ARCADE VAULT · {sys["name"].upper()} · {len(games)} GAMES</div>
</body>
</html>
'''

# ══════════════════════════════════════════════
#  ROOT INDEX.HTML — main menu, HTML+CSS only
# ══════════════════════════════════════════════
def make_root_index(sys_data):
    """sys_data = list of (sys, count)"""
    cards = ''
    for (sys, count) in sys_data:
        col   = sys['color']
        bios_badge = '<div class="sys-badge bios">BIOS</div>' if sys['bios'] else ''
        cnt_class  = ' has' if count else ''
        cnt_label  = f'{count} ROM' if count else '+ ROM'
        cards += f'''
    <a class="sys-card" href="systems/{sys["id"]}/index.html"
       style="--c:{col};--bg2:{sys["bg"]}">
      {bios_badge}
      <span class="sys-ico">{sys["ico"]}</span>
      <div class="sys-name">{sys["name"]}</div>
      <div class="sys-full">{sys["full"]}</div>
      <div class="sys-foot">
        <span class="sys-year">{sys["year"]}</span>
        <span class="sys-count{cnt_class}">{cnt_label}</span>
      </div>
    </a>'''

    total_games = sum(c for _, c in sys_data)
    total_sys   = len([s for s, c in sys_data if c > 0])

    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#07071c">
<title>🕹️ Arcade Vault</title>
<style>
{BASE_CSS}

/* hero */
.hero{{text-align:center;padding:36px 16px 28px;position:relative;z-index:1}}
.hero-badge{{display:inline-flex;align-items:center;gap:6px;
  padding:4px 14px;border-radius:14px;
  border:1px solid rgba(136,0,255,.28);background:rgba(136,0,255,.06);
  font-family:var(--fd);font-size:8px;letter-spacing:2.5px;color:#9966ff;
  margin-bottom:14px}}
.hero-badge::before{{content:'';width:5px;height:5px;border-radius:50%;
  background:#9966ff;animation:pulse 2s ease infinite}}
.hero h1{{font-family:var(--fd);font-size:clamp(36px,12vw,72px);font-weight:700;
  line-height:.9;letter-spacing:2px;
  background:linear-gradient(135deg,#ff0088 0%,#8800ff 45%,#00ffcc 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin-bottom:4px}}
.hero h2{{font-family:var(--fd);font-size:clamp(12px,4vw,20px);
  letter-spacing:8px;color:var(--mt);margin-bottom:20px;font-weight:400}}
.hero-stats{{display:inline-flex;gap:28px;
  border:1px solid rgba(255,255,255,.06);border-radius:12px;
  background:rgba(255,255,255,.02);padding:10px 22px}}
.stat-n{{font-family:var(--fd);font-size:20px;font-weight:700;color:#fff;
  background:linear-gradient(135deg,#aa44ff,#ff44aa);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.stat-l{{font-size:7px;letter-spacing:2px;color:var(--mt)}}

/* section label */
.sys-label{{max-width:900px;margin:0 auto;padding:8px 16px 12px;
  display:flex;align-items:center;gap:8px}}
.sys-label-line{{flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.06),transparent)}}
.sys-label-txt{{font-family:var(--fd);font-size:8px;letter-spacing:3px;color:var(--mt)}}

/* hint box */
.hint{{max-width:900px;margin:8px auto 20px;padding:0 12px}}
.hint-inner{{background:rgba(0,204,85,.05);border:1px solid rgba(0,204,85,.15);
  border-radius:10px;padding:12px 16px;
  font-family:var(--fd);font-size:10px;color:rgba(0,204,85,.7);
  line-height:1.7;letter-spacing:.3px;text-align:center}}
.hint-inner code{{background:rgba(0,204,85,.1);padding:1px 5px;
  border-radius:3px;color:#00cc55;border:1px solid rgba(0,204,85,.2)}}
</style>
</head>
<body>

<!-- TOP BAR -->
<div class="topbar">
  <div class="tb-inner">
    <div class="logo-wrap">
      <div class="logo-box">🕹️</div>
      <div class="logo-name">ARCADE VAULT</div>
    </div>
    <div class="tb-mid"></div>
    <div class="tb-right">
      <div class="tb-dot"></div>
      <span>LOCAL · HTTP</span>
    </div>
  </div>
</div>

<!-- HERO -->
<div class="hero">
  <div class="hero-badge">RETRO GAMING VAULT</div>
  <h1>ARCADE</h1>
  <h2>V A U L T</h2>
  <div class="hero-stats">
    <div><div class="stat-n">{len(SYSTEMS)}</div><div class="stat-l">SYSTEMS</div></div>
    <div><div class="stat-n">{total_games}</div><div class="stat-l">GAMES</div></div>
    <div><div class="stat-n">{total_sys}</div><div class="stat-l">ACTIVE</div></div>
  </div>
</div>

<!-- HINT -->
<div class="hint">
  <div class="hint-inner">
    لإضافة لعبة: ضع الروم في <code>systems/[id]/roms/</code> ثم شغّل <code>python scan.py</code>
  </div>
</div>

<!-- SYSTEMS GRID -->
<div class="sys-label">
  <div class="sys-label-line"></div>
  <div class="sys-label-txt">SELECT SYSTEM</div>
  <div class="sys-label-line"></div>
</div>
<div class="sys-grid">
  {cards}
</div>

<div class="footer">ARCADE VAULT · {len(SYSTEMS)} SYSTEMS · HTML+CSS · NO JS LAUNCHER</div>
</body>
</html>
'''

# ══════════════════════════════════════════════
#  MAIN SCAN
# ══════════════════════════════════════════════
def scan():
    print('🎮 Arcade Vault v8 — ROM Scanner')
    print('='*44)

    SYSDIR.mkdir(exist_ok=True)
    sys_data = []
    total_games = 0

    for sys in SYSTEMS:
        sid     = sys['id']
        sys_dir = SYSDIR / sid
        rom_dir = sys_dir / 'roms'
        sys_dir.mkdir(exist_ok=True)
        rom_dir.mkdir(exist_ok=True)
        if sys['bios']:
            (sys_dir / 'bios').mkdir(exist_ok=True)

        # Scan ROMs
        valid_exts = set(sys['exts'])
        games = []
        if rom_dir.exists():
            for f in sorted(rom_dir.iterdir()):
                if not f.is_file(): continue
                ext = f.suffix.lower()
                if ext not in valid_exts: continue
                name = f.stem
                games.append(dict(
                    name  = name,
                    file  = f.name,
                    slug  = slug(name),
                    ext   = ext,
                    size  = f.stat().st_size,
                    path  = f'systems/{sid}/roms/{f.name}'
                ))

        # Find BIOS
        bios_path = find_bios(sys_dir, sys['bios'])

        # Generate per-game player.html files
        for g in games:
            player_html = make_player(
                rom_name = g['name'],
                rom_file = g['path'],
                sys      = sys,
                bios_path = bios_path,
                depth    = 2
            )
            player_path = sys_dir / f'{g["slug"]}.html'
            player_path.write_text(player_html, encoding='utf-8')

        # Generate system index.html
        sys_index = make_sys_index(sys, games)
        (sys_dir / 'index.html').write_text(sys_index, encoding='utf-8')

        count = len(games)
        total_games += count
        sys_data.append((sys, count))

        if count:
            print(f'  ✅ {sid:10s} — {count:3d} لعبة')
        else:
            print(f'  ⬜ {sid:10s} — لا توجد ألعاب')

    # Generate root index.html
    root_index = make_root_index(sys_data)
    (BASE / 'index.html').write_text(root_index, encoding='utf-8')

    print('='*44)
    print(f'\n✅ المجموع: {total_games} لعبة في {sum(1 for _,c in sys_data if c)} نظام')
    print(f'✅ index.html + {len(SYSTEMS)} system pages')
    print(f'\n🌐 افتح في المتصفح: http://localhost:8080/index.html')

if __name__ == '__main__':
    scan()
    input('\nاضغط Enter للإغلاق...')
