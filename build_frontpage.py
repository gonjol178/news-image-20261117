#!/usr/bin/env python3
"""Compose the 17 Nov 2026 front page: panels + crisp PIL-rendered headlines."""
from PIL import Image, ImageDraw, ImageFont
import os

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')

SERIF_B = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 16, 12)
GREY = (84, 78, 68)
RULE = (20, 16, 12)
ACCENT = (146, 22, 22)

img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

def fit(img_src, w, h):
    """Center-crop image to cover w x h, return resized copy."""
    iw, ih = img_src.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    r = img_src.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return r.crop((x, y, x + w, y + h))

def panel(name, x, y, w, h):
    p = Image.open(os.path.join(A, name)).convert('RGB')
    img.paste(fit(p, w, h), (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)

def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

M = 26  # margin

# ---------- masthead ----------
y = 18
d.text((W // 2, y), 'T H E   W O R L D   I N   O N E   D A Y', font=font(SANS_B, 21),
       fill=ACCENT, anchor='ma')
y += 34
d.line([M, y, W - M, y], fill=RULE, width=3)
y += 10
d.text((W // 2, y), 'TUESDAY, 17 NOVEMBER 2026', font=font(SERIF_B, 55), fill=INK, anchor='ma')
y += 74
d.line([M, y, W - M, y], fill=RULE, width=3)
y += 12

# ---------- lead story ----------
panel('media-generation-panel-bridge-0-acb737ff-53be-48f0-830e-259dfd6622f8.webp', M, y, W - 2 * M, 268)
y += 280
for ln in wrap('UKRAINE SHATTERS THE CRIMEA BRIDGE', font(SERIF_B, 44), W - 2 * M):
    d.text((M, y), ln, font=font(SERIF_B, 44), fill=INK)
    y += 52
for ln in wrap("Zelenskyy hails an 'unprecedented' strike on Russia's lifeline to Crimea; "
               "Moscow answers with attacks on Kyiv's bridges", font(SANS, 20), W - 2 * M):
    d.text((M, y), ln, font=font(SANS, 20), fill=GREY)
    y += 27
y += 8
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 12

# ---------- middle row: radar + summit ----------
colw = (W - 2 * M - 16) // 2
panel('media-generation-panel-radar-0-4145fd3b-11b9-4d8d-b5f2-abff16313d79.webp', M, y, colw, 146)
panel('media-generation-panel-summit-0-43455db6-e1cc-4736-96be-9e90666b4b9c.webp', M + colw + 16, y, colw, 146)
y += 156
cap_y = y
for ln in wrap("IRAN'S DRONES TARGET U.S. RADAR IN BAHRAIN", font(SANS_B, 22), colw):
    d.text((M, cap_y), ln, font=font(SANS_B, 22), fill=INK); cap_y += 28
for ln in wrap('Attack intercepted, no casualties reported; Washington alleges a wider Iranian plot',
               font(SANS, 16), colw):
    d.text((M, cap_y), ln, font=font(SANS, 16), fill=GREY); cap_y += 21
cap2_y = y
for ln in wrap('TRUMP IN ASIA FOR APEC TALKS', font(SANS_B, 22), colw):
    d.text((M + colw + 16, cap2_y), ln, font=font(SANS_B, 22), fill=INK); cap2_y += 28
for ln in wrap('Leaders gather in China ahead of expected talks with Xi and Putin',
               font(SANS, 16), colw):
    d.text((M + colw + 16, cap2_y), ln, font=font(SANS, 16), fill=GREY); cap2_y += 21
y = max(cap_y, cap2_y) + 8
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 12

# ---------- bottom row: two text columns ----------
for ln in wrap('JAPAN SCRAMBLES JETS AS RUSSIAN PLANES ENTER ITS AIRSPACE', font(SANS_B, 20), colw):
    d.text((M, y), ln, font=font(SANS_B, 20), fill=INK); y += 26
d.text((M, y), 'Tokyo protests the early-morning incursion', font=font(SANS, 16), fill=GREY)
tx = M + colw + 16
ty = y - 52
items = [
    ('FRANCE', 'Second nationwide strike over pay'),
    ('GENEVA', '128 states debate banning killer robots'),
    ('GAZA', 'Allies urge Israel to open aid crossings'),
]
for head, body in items:
    d.text((tx, ty), head + ' \u2014 ', font=font(SANS_B, 16), fill=ACCENT)
    hw = d.textlength(head + ' \u2014 ', font=font(SANS_B, 16))
    d.text((tx + hw, ty), body, font=font(SANS, 16), fill=INK)
    ty += 26

# ---------- footer ----------
d.line([M, H - 44, W - M, H - 44], fill=RULE, width=3)
d.text((W // 2, H - 36), 'ONE DAY • ONE PAGE • THE WORLD ON TUESDAY 17 NOVEMBER 2026',
       font=font(SANS_B, 16), fill=GREY, anchor='ma')

img.save(OUT)
print('saved', OUT, img.size, os.path.getsize(OUT), 'bytes')
