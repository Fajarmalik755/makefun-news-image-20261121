#!/usr/bin/env python3
"""Build the news-image-20261121 entry: one 1024x1024 poster summing up
Saturday 21 November 2026 world news. Written from scratch for this
competition. Run: python3 main.py  ->  entry.png
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14

# ---------------------------------------------------------------- palette
NAVY = (11, 31, 58)
NAVY2 = (18, 46, 82)
RED = (200, 16, 46)
RED_DK = (160, 10, 36)
GOLD = (255, 210, 63)
INK = (20, 33, 61)
MUTED = (90, 107, 132)
FAINT = (140, 152, 170)
PAPER = (255, 255, 255)
LIGHT = (242, 244, 247)
LINE = (214, 221, 231)
GREEN = (27, 140, 90)
TEAL = (13, 148, 136)
ORANGE = (234, 88, 12)
SKY = (2, 132, 199)
PURPLE = (109, 40, 217)

# ---------------------------------------------------------------- fonts
def font(name, size):
    # Bundled fonts ship in fonts/ next to this script so the program does
    # not depend on the sandbox having any system fonts installed.
    here = os.path.dirname(os.path.abspath(__file__))
    bundled = {
        "bold": os.path.join(here, "fonts", "NotoSans-Bold.ttf"),
        "reg": os.path.join(here, "fonts", "NotoSans-Regular.ttf"),
        "it": os.path.join(here, "fonts", "NotoSans-Italic.ttf"),
        "serif": os.path.join(here, "fonts", "NotoSerif-Bold.ttf"),
        "serifreg": os.path.join(here, "fonts", "NotoSerif-Regular.ttf"),
    }
    paths = {
        "bold": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "reg": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "it": "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf",
        "serif": "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
        "serifreg": "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    }
    fb = {
        "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "reg": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "it": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serifreg": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    }
    for cand in (bundled[name], paths[name], fb[name]):
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()

F = {
    "mast": font("serif", 40),
    "kick": font("bold", 15),
    "tick": font("bold", 14),
    "stat_n": font("bold", 21),
    "stat_l": font("bold", 9),
    "chip": font("bold", 12),
    "hero_k": font("bold", 10),
    "hero_h": font("bold", 19),
    "hero_b": font("reg", 12),
    "hero_s": font("it", 10),
    "sm_k": font("bold", 9),
    "sm_h": font("bold", 13),
    "sm_b": font("reg", 11),
    "sm_s": font("it", 9),
    "also_h": font("bold", 12),
    "also": font("reg", 11),
    "map_h": font("bold", 12),
    "map_l": font("bold", 9),
    "tl": font("reg", 11),
    "dc_h": font("bold", 11),
    "dc": font("reg", 10),
    "src": font("reg", 10),
}

# ---------------------------------------------------------------- text utils
def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def block(d, x, y, lines, fnt, color, lh=None, max_lines=None):
    lh = lh or int(fnt.size * 1.25)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y

def text_w(d, text, fnt):
    return d.textlength(text, font=fnt)

# ---------------------------------------------------------------- data
HEROES = [
    dict(kick="NEW YORK · MARKETS", tag="AMERICAS",
         head="WALL STREET'S WORST WEEK SINCE 2020",
         body="S&P -3.7%, Nasdaq -5.28%, Dow -1.9%: the worst week since 2020. Nvidia -13.8%.",
         src="BlockBeats · Barron's · QNC News", color=RED, art="chart"),
    dict(kick="ANTALYA · CLIMATE", tag="EUROPE",
         head="COP31: NO DEAL AS TALKS SLIP INTO OVERTIME",
         body="Talks slipped past Friday's deadline with no deal. A third draft is due Saturday morning.",
         src="AP · AsiaToday · Fast Company", color=TEAL, art="climate"),
    dict(kick="WELLINGTON · CRICKET", tag="OCEANIA",
         head="RAHUL'S CENTURY PUTS INDIA ON TOP",
         body="Rahul made 100 off 207 balls, his 13th Test ton — a first for an Indian opener in SENA Tests.",
         src="Reuters · SportsTak · AP", color=GREEN, art="cricket"),
]

SMALL = [
    dict(kick="ODISHA · CYCLONE", tag="ASIA", head="AKVAN AFTERMATH: ZERO DEATHS",
         body="Zero deaths, 372,000 evacuated; 1,450 babies born in shelters, all safe.",
         src="The Ridhu Times · Dot Times", color=SKY, art="cyclone"),
    dict(kick="MERCURY · SPACE", tag="EUROPE", head="BEPICOLOMBO BURNS TONIGHT",
         body="Tonight 19:24 CET: a 37-minute burn to be caught by Mercury's gravity.",
         src="ESA · Sky & Telescope", color=PURPLE, art="space"),
    dict(kick="LAS VEGAS · FORMULA 1", tag="AMERICAS", head="NORRIS ON POLE IN THE RAIN",
         body="Norris took pole in the rain, 1:47.934; Verstappen 2nd, Hamilton last.",
         src="AP · f1dreaming.com", color=ORANGE, art="f1"),
    dict(kick="NAIROBI · MINING", tag="AFRICA", head="KENYA'S $60BN MINERALS DEAL",
         body="US-backed ReElement won the Mrima Hill deal, beating Chinese rivals.",
         src="BBC News", color=GOLD, art="mining"),
    dict(kick="WASHINGTON · SCIENCE", tag="AMERICAS", head="NASA'S $171M FOR 302 FIRMS",
         body="NASA picked 302 small firms for up to $171m, backing Artemis.",
         src="CASRAI · NASA", color=NAVY2, art="rocket"),
    dict(kick="COPENHAGEN · JUSTICE", tag="EUROPE", head="DANES CHARGED IN RUSSIA PLOT",
         body="Two Danes charged over an alleged Russian plot to kill a rapper.",
         src="La Méditerranée", color=RED, art="scales"),
    dict(kick="BRUSSELS · SECURITY", tag="EUROPE", head="NATO FOR LAND? US PLAN",
         body="The US reportedly offered Ukraine NATO membership for land.",
         src="La Méditerranée", color=NAVY2, art="shield"),
    dict(kick="KYIV · WAR", tag="EUROPE", head="RUSSIA HAS LOST 1.6M TROOPS",
         body="Defence officials say Russia has lost 1.6 million troops.",
         src="La Méditerranée", color=MUTED, art="helmet"),
    dict(kick="WASHINGTON · DEFENCE", tag="MIDEAST", head="IRAN CAMPAIGN COST $48.3BN",
         body="America's Iran campaign has cost $48.3bn since 28 February.",
         src="La Méditerranée", color=ORANGE, art="dollar"),
    dict(kick="LOS ANGELES · MOTORS", tag="ASIA", head="2027 ELANTRA UNVEILED IN LA",
         body="Hyundai unveiled the 2027 Elantra, with a hybrid, in Los Angeles.",
         src="Jagran Josh", color=TEAL, art="car"),
    dict(kick="THE HAGUE · JUSTICE", tag="ASIA", head="SWISS HAIL MYANMAR RULING",
         body="Switzerland called the Myanmar ruling an 'important step'.",
         src="La Méditerranée", color=SKY, art="court"),
    dict(kick="MARS · SPACE", tag="GLOBAL", head="NASA PAUSES MARS MISSIONS",
         body="NASA paused science on Perseverance and Mars Odyssey.",
         src="CASRAI · NASA", color=RED_DK, art="rover"),
]

ALSO = [
    "S&P 500 now in correction, over 10% below its 6 October high.",
    "Nikkei and Kospi fell more than 5% overnight in Asia.",
    "Brent $92.57 · 10-year Treasury 4.93% · VIX 35.89.",
    "Bitcoin below $60,000 for a seventh straight weekly drop.",
    "Anthropic falls 8.5% on its second day after its IPO.",
    "COP31: median finish late Sunday night, Carbon Brief finds.",
    "Spain strike: Amnesty says police used excessive force.",
    "Italy hit by protests against the Meloni government.",
    "Brazil strengthens Indigenous land protection with Raoni.",
    "Ukraine to provide food aid to nine countries.",
    "UN: Saudi-led attacks on Hudaydah threaten the aid lifeline.",
    "German defence official open to talks with the Kremlin.",
    "US panel: India targeting minorities in voter rolls.",
    "Nearly 600 women killed in South Africa in three months.",
    "Dozens missing after a migrant boat sinks off Senegal.",
    "Nigeria moves to end jail terms for attempted suicide.",
    "Nikhil Gupta jailed 19+ years in the Pannun plot.",
    "GAO: mental-health AI chatbots escape FDA oversight.",
    "UT Austin launches the Horizon supercomputer, 24th on TOP500.",
    "F1 Academy: Palmowski takes a record pole in Las Vegas.",
]

STATS = [
    ("-3.7%", "S&P 500 FRIDAY"),
    ("-5.28%", "NASDAQ FRIDAY"),
    ("$59,149", "BITCOIN"),
    ("372,000", "EVACUATED · ODISHA"),
    ("100", "RAHUL RUNS · 207 BALLS"),
    ("1.6M", "RUSSIAN TROOPS LOST"),
]

CHIPS = [("ASIA", 6, SKY), ("MIDEAST", 2, ORANGE), ("EUROPE", 9, TEAL),
         ("AFRICA", 4, GREEN), ("AMERICAS", 11, RED), ("OCEANIA", 1, GOLD),
         ("GLOBAL", 2, PURPLE)]

TIMELINE = [
    ("00:03 UTC", "BBC leads with Kenya's $60bn minerals deal."),
    ("00:19 UTC", "Reuters: Rahul reaches his century in Wellington."),
    ("01:22 UTC", "BlockBeats: Wall Street's worst week since 2020."),
    ("04:00 UTC", "Norris takes pole in wet Las Vegas qualifying."),
    ("19:24 CET", "BepiColombo fires its thrusters for Mercury orbit."),
    ("20:00 PST", "Las Vegas Grand Prix lights out; Norris on pole."),
]

DATECHECK = [
    "Poland: Russian missiles and a drone came down in the south-east · Russia fired 400+ drones at Ukraine · Mongolia's president resigned.",
    "JPMorgan, Visa and Mastercard disclosed a vendor cyberattack on 19 Nov · Cyclone Akvan made landfall on 20 Nov.",
]

SOURCES = ("Sources: Reuters · AP · BBC · BlockBeats · Barron's · Sky & Telescope · ESA · F1 Academy · "
           "La Méditerranée · CASRAI — All stories first reported on Saturday 21 November 2026.")

# ---------------------------------------------------------------- illustrations
def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)

def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 32))
    for i in range(5):
        gy = y + 8 + i * (h - 16) // 4
        d.line([x + 8, gy, x + w - 8, gy], fill=(255, 255, 255, 40) if False else (58, 58, 72), width=1)
    bars = [(0.10, 0.30), (0.24, 0.42), (0.38, 0.34), (0.52, 0.55), (0.66, 0.62), (0.80, 0.72)]
    bw = w * 0.07
    for fx, fy in bars:
        bx = x + fx * w
        top = y + fy * h
        d.rectangle([bx, top, bx + bw, y + h - 12], fill=RED)
        d.line([bx + bw / 2, y + (fy - 0.08) * h, bx + bw / 2, top], fill=RED, width=2)
    d.line([x + 10, y + 14, x + w * 0.45, y + h * 0.45, x + w - 14, y + h - 16],
           fill=GOLD, width=4)
    d.polygon([(x + w - 14, y + h - 16), (x + w - 30, y + h - 26), (x + w - 26, y + h - 8)],
              fill=GOLD)

def art_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 74, 66))
    d.ellipse([x + w * 0.62, y + 8, x + w * 0.92, y + h * 0.55], fill=GOLD)
    d.ellipse([x + w * 0.10, y + h * 0.42, x + w * 0.48, y + h * 1.05], fill=(46, 160, 140))
    d.arc([x + w * 0.10, y + h * 0.42, x + w * 0.48, y + h * 1.05], 180, 360, fill=(255, 255, 255), width=2)
    for fx, fc in [(0.58, RED), (0.70, (255, 255, 255)), (0.82, GOLD)]:
        px = x + fx * w
        d.line([px, y + h * 0.55, px, y + h - 10], fill=(255, 255, 255), width=2)
        d.polygon([(px, y + h * 0.55), (px + 18, y + h * 0.62), (px, y + h * 0.70)], fill=fc)

def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 92, 52))
    d.rectangle([x + w * 0.30, y, x + w * 0.70, y + h], fill=(58, 140, 90))
    for sx in (0.40, 0.45, 0.50):
        d.line([x + sx * w, y + 8, x + sx * w, y + 34], fill=(255, 235, 180), width=3)
    d.ellipse([x + w * 0.68, y + h * 0.55, x + w * 0.80, y + h * 0.78], fill=(200, 30, 30))
    d.polygon([(x + w * 0.22, y + h * 0.30), (x + w * 0.30, y + h * 0.22),
               (x + w * 0.42, y + h * 0.72), (x + w * 0.34, y + h * 0.78)], fill=(210, 170, 110))
    d.text((x + 8, y + h - 24), "100*", font=font("bold", 20), fill=(255, 255, 255))

def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 60, 110))
    cx, cy = x + w * 0.5, y + h * 0.52
    for r in range(6, int(min(w, h) * 0.55), 6):
        d.arc([cx - r, cy - r, cx + r, cy + r], r * 22, r * 22 + 260,
              fill=(255, 255, 255), width=2)
    for i in range(6):
        rx = x + 10 + i * (w - 20) // 5
        d.line([rx, y + 6, rx - 4, y + 16], fill=(180, 210, 255), width=2)

def art_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 12, 40))
    for sx, sy in [(0.15, 0.2), (0.3, 0.12), (0.55, 0.25), (0.8, 0.15), (0.9, 0.4), (0.4, 0.35)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1], fill=(255, 255, 255))
    d.ellipse([x + w * 0.58, y + h * 0.35, x + w * 0.98, y + h * 1.05], fill=(214, 120, 40))
    d.ellipse([x + w * 0.66, y + h * 0.48, x + w * 0.78, y + h * 0.68], fill=(170, 85, 25))
    d.polygon([(x + w * 0.18, y + h * 0.55), (x + w * 0.30, y + h * 0.35),
               (x + w * 0.42, y + h * 0.55), (x + w * 0.30, y + h * 0.62)], fill=(200, 205, 215))
    d.polygon([(x + w * 0.24, y + h * 0.60), (x + w * 0.30, y + h * 0.78),
               (x + w * 0.36, y + h * 0.60)], fill=GOLD)
    d.line([x + w * 0.30, y + h * 0.35, x + w * 0.30, y + h * 0.18], fill=(200, 205, 215), width=2)

def art_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 26))
    sq = max(6, h // 4)
    for r in range(2):
        for c in range(int(w // sq) + 1):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * sq, y + r * sq, x + (c + 1) * sq, y + (r + 1) * sq],
                            fill=(255, 255, 255))
    cy = y + h * 0.62
    d.polygon([(x + w * 0.08, cy), (x + w * 0.22, cy - 8), (x + w * 0.55, cy - 8),
               (x + w * 0.68, cy + 2), (x + w * 0.92, cy + 2), (x + w * 0.94, cy + 12),
               (x + w * 0.10, cy + 12)], fill=RED)
    d.ellipse([x + w * 0.24, cy + 8, x + w * 0.34, cy + 18], fill=(10, 10, 12))
    d.ellipse([x + w * 0.72, cy + 8, x + w * 0.82, cy + 18], fill=(10, 10, 12))
    d.text((x + 8, y + h - 22), "1:47.934", font=font("bold", 15), fill=GOLD)

def art_mining(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 62, 20))
    d.polygon([(x + w * 0.15, y + h), (x + w * 0.35, y + h * 0.25), (x + w * 0.55, y + h)], fill=(60, 38, 12))
    d.polygon([(x + w * 0.55, y + h), (x + w * 0.72, y + h * 0.35), (x + w * 0.90, y + h)], fill=(60, 38, 12))
    for cx, cy, c in [(0.30, 0.45, (120, 200, 255)), (0.45, 0.30, (255, 255, 255)), (0.68, 0.50, (120, 200, 255))]:
        d.polygon([(x + cx * w, y + cy * h - 12), (x + cx * w + 8, y + cy * h),
                   (x + cx * w, y + cy * h + 12), (x + cx * w - 8, y + cy * h)], fill=c)

def art_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 32, 64))
    for sx, sy in [(0.12, 0.2), (0.85, 0.18), (0.7, 0.4), (0.2, 0.55)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1], fill=(255, 255, 255))
    cx = x + w * 0.5
    d.polygon([(cx, y + 8), (cx + 12, y + h * 0.45), (cx - 12, y + h * 0.45)], fill=(255, 255, 255))
    d.rectangle([cx - 12, y + h * 0.45, cx + 12, y + h * 0.68], fill=(200, 16, 46))
    d.ellipse([cx - 6, y + h * 0.48, cx + 6, y + h * 0.60], fill=SKY)
    d.polygon([(cx - 12, y + h * 0.68), (cx - 20, y + h * 0.82), (cx - 12, y + h * 0.78)], fill=RED)
    d.polygon([(cx + 12, y + h * 0.68), (cx + 20, y + h * 0.82), (cx + 12, y + h * 0.78)], fill=RED)
    d.polygon([(cx - 5, y + h * 0.68), (cx, y + h * 0.95), (cx + 5, y + h * 0.68)], fill=GOLD)

def art_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 230))
    cx, cy = x + w * 0.5, y + h * 0.28
    d.line([cx, cy, cx, y + h * 0.82], fill=INK, width=3)
    d.line([x + w * 0.18, cy + 4, x + w * 0.82, cy + 4], fill=INK, width=3)
    for sgn in (-1, 1):
        px = cx + sgn * w * 0.32
        d.line([px, cy + 4, px, y + h * 0.55], fill=INK, width=2)
        d.polygon([(px - 14, y + h * 0.55), (px + 14, y + h * 0.55), (px, y + h * 0.78)], fill=GOLD)
    d.rectangle([x + w * 0.38, y + h * 0.82, x + w * 0.62, y + h * 0.88], fill=INK)

def art_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 46, 82))
    cx = x + w * 0.5
    d.polygon([(cx - 22, y + 8), (cx + 22, y + 8), (cx + 22, y + h * 0.55),
               (cx, y + h - 6), (cx - 22, y + h * 0.55)], fill=(255, 255, 255))
    d.polygon([(cx - 15, y + 14), (cx + 15, y + 14), (cx + 15, y + h * 0.52),
               (cx, y + h - 12), (cx - 15, y + h * 0.52)], fill=NAVY2)
    # small gold star, drawn (no glyph dependency)
    sx, sy = cx, y + h * 0.32
    star = []
    for i in range(10):
        rad = 7 if i % 2 == 0 else 3
        a = math.radians(-90 + i * 36)
        star.append((sx + rad * math.cos(a), sy + rad * math.sin(a)))
    d.polygon(star, fill=GOLD)

def art_helmet(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 241))
    cx, cy = x + w * 0.5, y + h * 0.45
    d.pieslice([cx - 22, cy - 18, cx + 22, cy + 18], 180, 360, fill=(90, 107, 132))
    d.rectangle([cx - 22, cy - 2, cx + 22, cy + 6], fill=(90, 107, 132))
    d.rectangle([cx - 26, cy + 6, cx + 26, cy + 10], fill=(60, 72, 90))
    d.text((x + 6, y + h - 20), "1.6M", font=font("bold", 15), fill=RED)

def art_dollar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 90, 52))
    d.text((x + w * 0.5 - 12, y + 2), "$", font=font("bold", 26), fill=GOLD)
    d.polygon([(x + w * 0.55, y + h * 0.72), (x + w * 0.75, y + h * 0.62),
               (x + w * 0.95, y + h * 0.72), (x + w * 0.75, y + h * 0.80)], fill=(255, 255, 255))

def art_car(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 90, 110))
    cy = y + h * 0.60
    d.polygon([(x + w * 0.10, cy), (x + w * 0.25, cy - 12), (x + w * 0.60, cy - 12),
               (x + w * 0.78, cy - 2), (x + w * 0.92, cy), (x + w * 0.92, cy + 10),
               (x + w * 0.10, cy + 10)], fill=(255, 255, 255))
    d.ellipse([x + w * 0.26, cy + 6, x + w * 0.36, cy + 16], fill=(10, 10, 12))
    d.ellipse([x + w * 0.68, cy + 6, x + w * 0.78, cy + 16], fill=(10, 10, 12))

def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 245))
    d.polygon([(x + w * 0.5, y + 6), (x + w * 0.92, y + h * 0.30), (x + w * 0.08, y + h * 0.30)],
              fill=NAVY)
    for fx in (0.20, 0.38, 0.56, 0.74):
        d.rectangle([x + fx * w - 3, y + h * 0.32, x + fx * w + 3, y + h * 0.82], fill=NAVY)
    d.rectangle([x + w * 0.10, y + h * 0.82, x + w * 0.90, y + h * 0.90], fill=NAVY)

def art_rover(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 16, 12))
    d.ellipse([x + w * 0.72, y + 6, x + w * 0.88, y + 22], fill=(255, 200, 150))
    d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.62), (x + w * 0.55, y + h * 0.80),
               (x + w * 0.80, y + h * 0.60), (x + w, y + h * 0.85), (x + w, y + h)],
              fill=(150, 70, 35))
    d.rectangle([x + w * 0.30, y + h * 0.42, x + w * 0.62, y + h * 0.58], fill=(210, 210, 215))
    for wx in (0.34, 0.46, 0.58):
        d.ellipse([x + wx * w - 5, y + h * 0.58, x + wx * w + 5, y + h * 0.68], fill=(30, 30, 34))
    d.line([x + w * 0.62, y + h * 0.45, x + w * 0.80, y + h * 0.30], fill=(210, 210, 215), width=2)

ARTS = {"chart": art_chart, "climate": art_climate, "cricket": art_cricket,
        "cyclone": art_cyclone, "space": art_space, "f1": art_f1,
        "mining": art_mining, "rocket": art_rocket, "scales": art_scales,
        "shield": art_shield, "helmet": art_helmet, "dollar": art_dollar,
        "car": art_car, "court": art_court, "rover": art_rover}

# ---------------------------------------------------------------- world map
# coarse land mask: (row, col_start, col_end) on a 96 x 13 dot grid
LAND = [
    (0, 2, 22), (0, 32, 42), (0, 49, 95),
    (1, 3, 33), (1, 45, 95),
    (2, 13, 32), (2, 45, 58), (2, 58, 85),
    (3, 14, 30), (3, 45, 56), (3, 60, 84),
    (4, 16, 28), (4, 45, 64), (4, 65, 81),
    (5, 20, 25), (5, 44, 61), (5, 66, 76),
    (6, 22, 26), (6, 44, 60), (6, 73, 76),
    (7, 26, 34), (7, 45, 58), (7, 73, 85),
    (8, 28, 38), (8, 50, 58), (8, 82, 88),
    (9, 29, 37), (9, 51, 57), (9, 78, 88),
    (10, 29, 33), (10, 52, 56), (10, 78, 88),
    (11, 29, 30), (11, 92, 95),
    (12, 29, 30),
]
MARKERS = [  # (lon, lat, label or None; side 'r' = label right of dot, 'l' = left)
    (-74, 41, "NEW YORK", "r"), (-115, 36, None, "r"), (174.8, -41.3, "WELLINGTON", "l"),
    (85, 20, "ODISHA", "r"), (30.7, 36.9, "ANTALYA", "r"), (36.8, -1.3, None, "r"),
    (12.6, 55.7, None, "r"), (51.4, 35.7, None, "r"),
]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 246))
    cols, rows = 96, 13
    cw, ch = w / cols, h / rows
    for r, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            cx, cy = x + (c + 0.5) * cw, y + (r + 0.5) * ch
            d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=(120, 135, 155))
    for lon, lat, label, side in MARKERS:
        c = (lon + 180) / 3.75
        r = (75 - lat) / 10
        cx, cy = x + (c + 0.5) * cw, y + (r + 0.5) * ch
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED, outline=(255, 255, 255), width=1)
        if label:
            if side == "l":
                d.text((cx - 6 - text_w(d, label, F["map_l"]), cy - 5), label,
                       font=F["map_l"], fill=RED)
            else:
                d.text((cx + 6, cy - 5), label, font=F["map_l"], fill=RED)

# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # ---- masthead (70)
    d.rectangle([0, 0, W, 70], fill=NAVY)
    d.rectangle([0, 66, W, 70], fill=RED)
    d.text((MARGIN, 10), "THE WORLD IN ONE IMAGE", font=F["mast"], fill=(255, 255, 255))
    date_txt = "SATURDAY · 21 NOVEMBER 2026"
    d.text((W - MARGIN - text_w(d, date_txt, F["kick"]), 14), date_txt,
           font=F["kick"], fill=GOLD)
    d.text((W - MARGIN - text_w(d, "35 STORIES · 7 REGIONS", F["kick"]), 36),
           "35 STORIES · 7 REGIONS", font=F["kick"], fill=(185, 198, 216))
    d.text((MARGIN, 52), "Every story below happened or was first reported today.",
           font=font("it", 12), fill=(185, 198, 216))
    y = 70

    # ---- ticker (20)
    d.rectangle([0, y, W, y + 20], fill=RED)
    tick = ("WALL STREET'S WORST WEEK SINCE 2020    •    COP31: NO DEAL    •    RAHUL 100*    •    "
            "BEPICOLOMBO TONIGHT    •    NORRIS ON POLE")
    d.text((MARGIN, y + 3), tick, font=F["tick"], fill=(255, 255, 255))
    y += 20

    # ---- stat bar (46)
    d.rectangle([0, y, W, y + 46], fill=PAPER)
    cw = (W - 2 * MARGIN) / 6
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + i * cw
        if i:
            d.line([cx, y + 8, cx, y + 38], fill=LINE, width=1)
        nw = text_w(d, num, F["stat_n"])
        d.text((cx + (cw - nw) / 2, y + 5), num, font=F["stat_n"],
               fill=RED if i in (0, 1) else INK)
        lw = text_w(d, lab, F["stat_l"])
        d.text((cx + (cw - lw) / 2, y + 30), lab, font=F["stat_l"], fill=MUTED)
    d.line([0, y + 46, W, y + 46], fill=LINE, width=1)
    y += 46

    # ---- region chips (24)
    d.rectangle([0, y, W, y + 24], fill=LIGHT)
    cx = MARGIN + 4
    d.text((cx, y + 5), "WHERE:", font=F["chip"], fill=MUTED)
    cx += text_w(d, "WHERE: ", F["chip"]) + 8
    for name, n, col in CHIPS:
        label = f"{name} {n}"
        wdt = text_w(d, label, F["chip"]) + 22
        d.ellipse([cx, y + 8, cx + 8, y + 16], fill=col)
        d.text((cx + 11, y + 5), label, font=F["chip"], fill=INK)
        cx += wdt + 10
    d.text((W - MARGIN - text_w(d, "35 STORIES TOTAL", F["chip"]), y + 5),
           "35 STORIES TOTAL", font=F["chip"], fill=RED)
    y += 24

    # ---- hero cards (200)
    gap = 8
    hw = (W - 2 * MARGIN - 2 * gap) // 3
    for i, st in enumerate(HEROES):
        x0 = MARGIN + i * (hw + gap)
        d.rectangle([x0, y, x0 + hw, y + 200], outline=LINE, width=1)
        ARTS[st["art"]](d, x0 + 1, y + 1, hw - 2, 80)
        d.rectangle([x0 + 1, y + 81, x0 + hw - 1, y + 200], fill=PAPER)
        d.text((x0 + 10, y + 85), st["kick"], font=F["hero_k"], fill=st["color"])
        ty = y + 98
        ty = block(d, x0 + 10, ty, wrap(d, st["head"], F["hero_h"], hw - 20),
                   F["hero_h"], INK, lh=21, max_lines=2)
        ty = block(d, x0 + 10, ty + 3, wrap(d, st["body"], F["hero_b"], hw - 20),
                   F["hero_b"], (52, 64, 84), lh=15, max_lines=3)
        d.text((x0 + 10, y + 200 - 13), "Source: " + st["src"], font=F["hero_s"], fill=FAINT)
    y += 200 + 6

    # ---- small cards (3 rows x 118)
    sw = (W - 2 * MARGIN - 3 * gap) // 4
    for r in range(3):
        for c in range(4):
            st = SMALL[r * 4 + c]
            x0 = MARGIN + c * (sw + gap)
            y0 = y + r * 118
            d.rectangle([x0, y0, x0 + sw, y0 + 118], outline=LINE, width=1)
            ARTS[st["art"]](d, x0 + 1, y0 + 1, sw - 2, 30)
            d.rectangle([x0 + 1, y0 + 31, x0 + sw - 1, y0 + 118], fill=PAPER)
            # region tag over the art strip, right side
            tag = st["tag"]
            tw = text_w(d, tag, F["sm_k"])
            d.rectangle([x0 + sw - tw - 12, y0 + 4, x0 + sw - 4, y0 + 18], fill=(255, 255, 255))
            d.text((x0 + sw - tw - 8, y0 + 5), tag, font=F["sm_k"], fill=st["color"])
            ty = y0 + 34
            d.text((x0 + 8, ty), st["kick"], font=F["sm_k"], fill=st["color"])
            block(d, x0 + 8, y0 + 47, wrap(d, st["head"], F["sm_h"], sw - 16),
                  F["sm_h"], INK, lh=15, max_lines=1)
            block(d, x0 + 8, y0 + 74, wrap(d, st["body"], F["sm_b"], sw - 16),
                  F["sm_b"], (52, 64, 84), lh=12, max_lines=2)
            d.text((x0 + 8, y0 + 118 - 12), "Source: " + st["src"], font=F["sm_s"], fill=FAINT)
    y += 3 * 118

    # ---- also on (136): header 16 + 10 rows x 12
    d.rectangle([0, y, W, y + 16], fill=NAVY)
    d.text((MARGIN, y + 2), "ALSO ON SATURDAY 21 NOVEMBER — 20 MORE STORIES",
           font=F["also_h"], fill=(255, 255, 255))
    y += 16
    col_w = (W - 2 * MARGIN - 16) // 2
    for i, item in enumerate(ALSO):
        col = i // 10
        row = i % 10
        x0 = MARGIN + col * (col_w + 16)
        yy = y + row * 12
        d.rectangle([x0, yy + 4, x0 + 5, yy + 9], fill=RED)
        d.text((x0 + 10, yy), item, font=F["also"], fill=INK)
    y += 10 * 12

    # ---- map + timeline (108)
    d.line([0, y, W, y], fill=LINE, width=1)
    map_w = 596
    d.text((MARGIN, y + 6), "WHERE IT HAPPENED", font=F["map_h"], fill=INK)
    draw_map(d, MARGIN, y + 24, map_w, 78)
    tx = MARGIN + map_w + 16
    d.line([tx - 8, y + 6, tx - 8, y + 102], fill=LINE, width=1)
    d.text((tx, y + 6), "21 NOVEMBER 2026 — AS THE DAY UNFOLDED",
           font=F["map_h"], fill=INK)
    ty = y + 24
    for t, txt in TIMELINE:
        d.text((tx, ty), t, font=font("bold", 11), fill=RED)
        d.text((tx + 74, ty), txt, font=F["tl"], fill=INK)
        ty += 14
    y += 108

    # ---- date check (48)
    d.rectangle([0, y, W, y + 48], fill=(255, 240, 242))
    d.rectangle([0, y, W, y + 48], outline=RED, width=1)
    d.text((MARGIN, y + 5), "DATE CHECK — FIRST REPORTED 20 NOVEMBER, NOT TODAY",
           font=F["dc_h"], fill=RED_DK)
    ty = y + 20
    for ln in DATECHECK:
        d.text((MARGIN, ty), ln, font=F["dc"], fill=(90, 30, 40))
        ty += 13
    y += 48

    # ---- sources (12)
    d.text((MARGIN, y + 1), SOURCES, font=F["src"], fill=MUTED)
    y += 12

    assert y == H, f"layout height {y} != {H}"
    # The server runs the program with the repo mounted read-only and names
    # the writable output directory via MAKEFUN_OUTPUT_DIR; locally (no env
    # var) write next to this script.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    img.save(dst)
    print(f"saved {dst} {W}x{H}, layout ends at y={y}")

if __name__ == "__main__":
    build()
