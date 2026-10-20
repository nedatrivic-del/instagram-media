"""Zahnärztin Altstadt – Reel / Karussell aus einer JSON-Spezifikation.

Aufruf:
  python3 make_media.py spec.json reel  OUT.mp4        # 9:16-Video (ca. 27 s)
  python3 make_media.py spec.json carousel OUTDIR      # 4:5-Slides slide_1.png ...
  python3 make_media.py spec.json preview OUTDIR       # Standbilder aller Reel-Szenen

Spec-Format: siehe ../posts/*/spec.json und AGENT.md.
"""
import json, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts") + "/"
PHOTO = os.path.join(HERE, "neda.jpg")

RED = (166, 41, 41); SLATE = (71, 82, 95); SAGE = (169, 202, 187)
MINT = (236, 246, 246); CREAM = (249, 247, 240); BLUSH = (239, 192, 182)
W, FPS = 1080, 30
INK = (71, 82, 95); BRAND_RED = (166, 41, 41)
THEME = "default"


def oswald(size, wght=300):
    f = ImageFont.truetype(F + "Oswald%5Bwght%5D.ttf", size)
    f.set_variation_by_axes([wght]); return f



def fira(size, style="Light"):
    return ImageFont.truetype(F + f"FiraSans-{style}.ttf", size)


def make_advent_bg(H):
    random.seed(11)
    top, bot = (28, 66, 52), (14, 38, 30)
    bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        f = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - f) + bot[i] * f) for i in range(3)))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 520, -260, W + 260, 420], fill=(214, 178, 110, 46)); gd.ellipse([-300, H - 420, 420, H + 300], fill=(190, 60, 50, 40))
    bg = Image.alpha_composite(bg.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(110)))
    st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    for _ in range(int(55 * H / 1920)):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.choice([2, 2, 3, 4])
        sd.ellipse([x - r, y - r, x + r, y + r], fill=(240, 214, 150, random.randint(60, 150)))
    bg.alpha_composite(st)
    noise = Image.effect_noise((W, H), 14).convert("L").point(lambda v: 128 + (v - 128) // 3)
    return Image.blend(bg.convert("RGB"), Image.merge("RGB", [noise] * 3), 0.035).convert("RGBA")


def make_bg(H):
    if THEME == "advent": return make_advent_bg(H)
    random.seed(7)
    bg = Image.new("RGB", (W, H), CREAM)
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(blob)
    k = H / 1920
    for (cx, cy, r, col, a) in [(980, 180, 320, BLUSH, 90), (120, 1750, 380, SAGE, 80),
                                (1000, 1500, 260, MINT, 160), (60, 420, 220, MINT, 150),
                                (850, 1850, 200, BLUSH, 70)]:
        cy = cy * k
        for _ in range(14):
            rr = r * random.uniform(0.5, 1.0); ox = random.uniform(-r * .4, r * .4); oy = random.uniform(-r * .4, r * .4)
            bd.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr], fill=col + (a // 4,))
    blob = blob.filter(ImageFilter.GaussianBlur(70))
    bg = Image.alpha_composite(bg.convert("RGBA"), blob)
    noise = Image.effect_noise((W, H), 14).convert("L").point(lambda v: 128 + (v - 128) // 3)
    return Image.blend(bg.convert("RGB"), Image.merge("RGB", [noise] * 3), 0.04).convert("RGBA")


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


_md = ImageDraw.Draw(Image.new("RGB", (10, 10)))


class Layer:
    def __init__(s, at, kind, **kw): s.at, s.kind, s.kw, s.y = at, kind, kw, 0

    def height(s):
        k = s.kw; maxw = k.get("maxw", W - 180)
        if s.kind == "text":
            return int(k["font"].size * k.get("lh", 1.2)) * len(wrap(_md, k["text"], k["font"], maxw))
        if s.kind == "rule": return 6
        if s.kind == "item":
            a = len(wrap(_md, k["title"], fira(46, "Medium"), maxw - 120)); b = len(wrap(_md, k["sub"], fira(44), maxw - 120))
            return max(84, 4 + 58 * a + 50 * b)
        return 0


def stack(spec, top, bottom):
    total = sum(L.height() + g for L, g in spec) - spec[-1][1]
    y = top + max(0, (bottom - top - total) // 2)
    for L, g in spec:
        L.y = y; y += L.height() + g
    return [L for L, _ in spec]


ANIM = 0.55


def draw_layer(img, t, L):
    p = ease((t - L.at) / ANIM)
    if p <= 0: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    a = int(255 * p); y = L.y + int((1 - p) * 40); k = L.kw; x = 90; maxw = k.get("maxw", W - 180)
    if L.kind == "text":
        for line in wrap(d, k["text"], k["font"], maxw):
            d.text((x, y), line, font=k["font"], fill=k["color"] + (a,)); y += int(k["font"].size * k.get("lh", 1.2))
    elif L.kind == "rule":
        d.rectangle([x, y, x + int(140 * p), y + 6], fill=SAGE + (a,))
    elif L.kind == "item":
        d.ellipse([x, y, x + 84, y + 84], fill=SAGE + (a,))
        nf = oswald(52, 400); tw = d.textlength(k["n"], font=nf)
        d.text((x + 42 - tw / 2, y + 6), k["n"], font=nf, fill=(255, 255, 255, a))
        yy = y + 4
        for line in wrap(d, k["title"], fira(46, "Medium"), maxw - 120):
            d.text((x + 120, yy), line, font=fira(46, "Medium"), fill=SLATE + (a,)); yy += 58
        for line in wrap(d, k["sub"], fira(44), maxw - 120):
            d.text((x + 120, yy), line, font=fira(44), fill=SLATE + (int(a * .85),)); yy += 50
    img.alpha_composite(layer)


def headline_layers(lines, t0=0.1, step=0.2, last_gap=44):
    """lines: [{"text":..., "size":110, "bold":false, "red":false, "maxw":900}]"""
    out = []
    for i, ln in enumerate(lines):
        f = oswald(ln.get("size", 110), 400 if ln.get("bold") else 300)
        out.append((Layer(t0 + i * step, "text", text=ln["text"].upper(), font=f, color=RED if ln.get("red") else SLATE,
                          maxw=ln.get("maxw", W - 180)), 0))
    out[-1] = (out[-1][0], last_gap)
    return out


class Builder:
    def __init__(s, spec, H):
        global THEME, SLATE, RED, SAGE
        THEME = spec.get("theme", "default")
        if THEME == "advent":
            SLATE, RED, SAGE = (247, 239, 222), (236, 112, 96), (214, 178, 110)
        s.spec, s.H = spec, H
        s.reel = H == 1920
        s.bg = make_bg(H)
        s.portrait = Image.open(PHOTO).convert("RGB")
        s.circ = None
        s.handle_y = 1600 if s.reel else H - 90
        s.zone = (260, 1520) if s.reel else (130, H - 140)

    def door(s, img):
        n = s.spec.get("door")
        if THEME != "advent" or not n: return
        d = ImageDraw.Draw(img); x1, y1 = W - 90, (150 if s.reel else 60); sz = 150
        d.rounded_rectangle([x1 - sz, y1, x1, y1 + sz], radius=22, outline=SAGE, width=5, fill=(20, 48, 38, 230))
        nf = oswald(84, 400); tw = d.textlength(str(n), font=nf)
        d.text((x1 - sz / 2 - tw / 2, y1 + 10), str(n), font=nf, fill=SAGE)
        lf = fira(22, "Regular"); lt = "TÜRCHEN"; d.text((x1 - sz / 2 - d.textlength(lt, font=lf) / 2, y1 + 112), lt, font=lf, fill=SAGE)

    def handle(s, img):
        s.door(img)
        ImageDraw.Draw(img).text((90, s.handle_y), "@dentistry.oldtown", font=fira(34, "Regular"), fill=SLATE + (178,))

    def hook(s, t, sc):
        img = s.bg.copy(); H = s.H
        ph_h = 1080 if s.reel else 760
        z = (1.0 + 0.12 * min(t / 3.0, 1)) if s.reel else 1.0
        pw, phh = s.portrait.size
        cw, ch = pw / z, pw / z * ph_h / W
        if ch > phh: ch = phh / z; cw = ch * W / ph_h
        cx0 = pw - cw - 10 * (1 - min(t, 4.5) / 4.5); cy0 = max(0, (phh - ch) * 0.25)
        crop = s.portrait.crop((int(cx0), int(cy0), int(cx0 + cw), int(cy0 + ch))).resize((W, ph_h), Image.LANCZOS).convert("RGBA")
        mask = Image.new("L", (W, ph_h), 255); md = ImageDraw.Draw(mask)
        for i in range(260):
            md.line([(0, ph_h - 260 + i), (W, ph_h - 260 + i)], fill=int(255 * (1 - i / 260)))
        pa = 1.0 if s.reel else ease(t / 0.6); mask = mask.point(lambda v: int(v * pa))
        img.paste(crop, (0, 0), mask)
        t0, st, tr, tsub = (-1.0, 0.0, -1.0, 0.5) if s.reel else (0.4, 0.3, 1.4, 1.6)
        spec = headline_layers(sc["lines"], t0, st, 34) + [(Layer(tr, "rule"), 40)]
        if sc.get("sub"):
            spec.append((Layer(tsub, "text", text=sc["sub"], font=fira(54, "LightItalic"), color=SLATE), 0))
        top, bottom = (1000, 1560) if s.reel else (ph_h - 80, H - 60)
        for L in stack(spec, top, bottom): draw_layer(img, t, L)
        s.door(img); return img

    def statement(s, t, sc):
        img = s.bg.copy(); spec = []
        if sc.get("kicker"):
            spec.append((Layer(0.1, "text", text=sc["kicker"], font=fira(52, "LightItalic"), color=RED), 24))
        spec += headline_layers(sc["lines"], 0.15, 0.12)
        spec += [(Layer(0.5, "rule"), 44), (Layer(0.7, "text", text=sc["body"], font=fira(56, "Light"), color=SLATE, lh=1.34), 0)]
        for L in stack(spec, *s.zone): draw_layer(img, t, L)
        s.handle(img); return img

    def tips(s, t, sc):
        img = s.bg.copy()
        spec = headline_layers(sc["lines"], 0.1, 0.15, 40) + [(Layer(0.5, "rule"), 56)]
        for i, it in enumerate(sc["items"]):
            spec.append((Layer(0.5 + 0.9 * i, "item", n=str(i + 1), title=it["title"], sub=it["sub"]), 54 if i < len(sc["items"]) - 1 else 0))
        for L in stack(spec, *s.zone): draw_layer(img, t, L)
        s.handle(img); return img

    def close(s, t, sc):
        img = s.bg.copy()
        if s.circ is None:
            sz = 300; pw, _ = s.portrait.size
            c = s.portrait.crop((int(pw * 0.50), 40, int(pw * 0.50) + 430, 470)).resize((sz, sz), Image.LANCZOS)
            m = Image.new("L", (sz * 4, sz * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, sz * 4, sz * 4], fill=255)
            s.circ = (c.convert("RGBA"), m.resize((sz, sz), Image.LANCZOS))
        spec = headline_layers(sc["lines"], 0.1, 0.15, 50) + [(Layer(0.5, "text", text=sc["body"], font=fira(52, "Light"), color=SLATE, lh=1.32), 0)]
        top, bottom = (230, 860) if s.reel else (50, 680)
        for L in stack(spec, top, bottom): draw_layer(img, t, L)
        p = ease((t - 1.0) / 0.5)
        if p > 0:
            card = Image.new("RGBA", (W, s.H), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
            a = int(255 * p); y0 = (920 if s.reel else 710) + int((1 - p) * 40)
            d.rounded_rectangle([90, y0, W - 90, y0 + 600], radius=44, fill=(255, 255, 255, int(a * .85)), outline=(246, 242, 226, a), width=6)
            c, m = s.circ
            card.paste(c, (130, y0 + 50), m.point(lambda v: int(v * p)))
            d.ellipse([126, y0 + 46, 434, y0 + 354], outline=SAGE + (a,), width=6)
            d.text((480, y0 + 95), "ZAHNÄRZTIN", font=oswald(66, 300), fill=INK + (a,))
            d.text((480, y0 + 170), "ALTSTADT", font=oswald(66, 300), fill=INK + (a,))
            d.text((480, y0 + 262), "Dr. med. dent. Neda Trivić", font=fira(34, "Regular"), fill=INK + (a,))
            d.text((480, y0 + 306), "Alle Kassen & Privat", font=fira(32, "Light"), fill=INK + (a,))
            d.text((130, y0 + 395), "Kapitelgasse 9 · Salzburger Altstadt", font=fira(38, "Light"), fill=INK + (a,))
            d.text((130, y0 + 445), "Terminvereinbarung online:", font=fira(38, "Medium"), fill=BRAND_RED + (a,))
            d.rounded_rectangle([130, y0 + 503, W - 130, y0 + 575], radius=36, fill=INK + (a,))
            txt = "termine.softdent.at/zahnaerztin-altstadt"; ff = fira(34, "Regular")
            d.text(((W - d.textlength(txt, font=ff)) / 2, y0 + 517), txt, font=ff, fill=(255, 255, 255, a))
            img.alpha_composite(card)
        s.door(img); return img

    def photo(s, t, sc):
        """Series "Ziemlich sympathisch, wenn ...": whole slide = analog photo print.
        Full photo with text on it (brand fonts), framed by a cream paper border; brand on the bottom strip."""
        from PIL import ImageOps, ImageEnhance
        H = s.H; key = sc["photo"]
        if not hasattr(s, "_ph"): s._ph = {}
        if key not in s._ph:
            s._ph[key] = ImageOps.exif_transpose(Image.open(os.path.join(HERE, "..", key))).convert("RGB")
        im = s._ph[key]
        bx, bt, bb = 46, 46, 150
        pw, ph = W - 2 * bx, H - bt - bb
        iw, ih = im.size; k = max(pw / iw, ph / ih)
        im2 = im.resize((int(iw * k) + 1, int(ih * k) + 1), Image.LANCZOS)
        fx, fy = sc.get("focus", [0.5, 0.5]); x0 = int((im2.width - pw) * fx); y0 = int((im2.height - ph) * fy)
        p_ = im2.crop((x0, y0, x0 + pw, y0 + ph))
        # analog look: faded contrast, warm tone, lifted blacks, grain, vignette
        p_ = ImageEnhance.Contrast(p_).enhance(0.9); p_ = ImageEnhance.Color(p_).enhance(0.85)
        r_, g_, b_ = p_.split()
        p_ = Image.merge("RGB", [r_.point(lambda v: int(16 + v * 0.94)), g_.point(lambda v: int(10 + v * 0.91)), b_.point(lambda v: int(4 + v * 0.84))])
        grain = Image.effect_noise((pw, ph), 22).convert("L")
        p_ = Image.blend(p_, Image.merge("RGB", [grain] * 3), 0.05)
        vig = Image.new("L", (pw, ph), 0); ImageDraw.Draw(vig).ellipse([-pw * .3, -ph * .25, pw * 1.3, ph * 1.25], fill=255)
        p_ = Image.composite(p_, Image.blend(p_, Image.new("RGB", (pw, ph), (50, 38, 26)), 0.28), vig.filter(ImageFilter.GaussianBlur(110)))
        p_ = p_.convert("RGBA")
        p_ = Image.alpha_composite(p_, Image.new("RGBA", (pw, ph), (20, 22, 26, 40)))
        # text on the photo (brand fonts), centred, with soft shade
        CRM = (250, 242, 222); GOLD = s.spec.get("frame_ink") == "gold"
        KCOL = (236, 204, 134) if GOLD else CRM; FINK = (156, 116, 44) if GOLD else SLATE
        kf = fira(62, "LightItalic"); tf = oswald(sc.get("size", 80), 300)
        d0 = ImageDraw.Draw(p_); lines = wrap(d0, sc["text"].upper(), tf, pw - 160)
        lh = int(tf.size * 1.18); hh = 86 + len(lines) * lh; y = (ph - hh) // 2 + sc.get("dy", 0)
        band = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        ImageDraw.Draw(band).rounded_rectangle([40, y - 80, pw - 40, y + hh + 60], radius=200, fill=(15, 16, 20, sc.get("shade", 120)))
        p_.alpha_composite(band.filter(ImageFilter.GaussianBlur(60)))
        lay = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        kick = sc.get("kicker", "Ziemlich sympathisch,")
        ld.text(((pw - ld.textlength(kick, font=kf)) / 2, y), kick, font=kf, fill=KCOL); y += 86
        for ln in lines:
            ld.text(((pw - ld.textlength(ln, font=tf)) / 2, y), ln, font=tf, fill=CRM); y += lh
        shadow = lay.split()[3].filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .6))
        p_.alpha_composite(Image.merge("RGBA", [Image.new("L", (pw, ph), 0)] * 3 + [shadow])); p_.alpha_composite(lay)
        # paper frame
        paper = Image.new("RGB", (W, H), (250, 247, 238))
        pn = Image.effect_noise((W, H), 10).convert("L")
        img = Image.blend(paper, Image.merge("RGB", [pn] * 3), 0.025).convert("RGBA")
        inner = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(inner).rectangle([bx - 2, bt - 2, bx + pw + 2, bt + ph + 2], fill=(0, 0, 0, 60))
        img.alpha_composite(inner.filter(ImageFilter.GaussianBlur(3)))
        img.alpha_composite(p_, (bx, bt))
        d = ImageDraw.Draw(img); by = bt + ph + 50
        bf = oswald(40, 300); brand = "ZAHNÄRZTIN ALTSTADT"
        d.text((bx + 4, by), brand, font=bf, fill=FINK)
        hf = fira(30, "LightItalic"); hd = "@dentistry.oldtown"
        d.text((W - bx - 4 - d.textlength(hd, font=hf), by + 8), hd, font=hf, fill=FINK)
        return img

    def framed(s, img):
        """Put any finished slide into the same analog paper frame as the photo series."""
        H = s.H; bx, bt, bb = 46, 46, 150; pw, ph = W - 2 * bx, H - bt - bb
        k = ph / H; sm = img.resize((int(W * k), ph), Image.LANCZOS)
        inner = s.bg.resize((pw, ph), Image.LANCZOS); inner.alpha_composite(sm.convert("RGBA"), ((pw - sm.width) // 2, 0))
        paper = Image.new("RGB", (W, H), (250, 247, 238)); pn = Image.effect_noise((W, H), 10).convert("L")
        out = Image.blend(paper, Image.merge("RGB", [pn] * 3), 0.025).convert("RGBA")
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([bx - 2, bt - 2, bx + pw + 2, bt + ph + 2], fill=(0, 0, 0, 60))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3))); out.alpha_composite(inner, (bx, bt))
        d = ImageDraw.Draw(out); by = bt + ph + 50
        d.text((bx + 4, by), "ZAHNÄRZTIN ALTSTADT", font=oswald(40, 300), fill=((156, 116, 44) if s.spec.get("frame_ink") == "gold" else SLATE))
        hf = fira(30, "LightItalic"); hd = "@dentistry.oldtown"
        d.text((W - bx - 4 - d.textlength(hd, font=hf), by + 8), hd, font=hf, fill=((156, 116, 44) if s.spec.get("frame_ink") == "gold" else SLATE))
        return out

    def scenes(s):
        durs = {"photo": 3.4, "hook": 3.2, "statement": 3.8, "tips": 5.4, "close": 4.2}
        out = []
        for sc in s.spec["scenes"]:
            fn = getattr(s, sc["type"])
            if sc.get("frame") and sc["type"] != "photo":
                out.append(((lambda t, fn=fn, sc=sc: s.framed(fn(t, sc))), sc.get("duration", durs[sc["type"]])))
            else:
                out.append(((lambda t, fn=fn, sc=sc: fn(t, sc)), sc.get("duration", durs[sc["type"]])))
        return out


def render_reel(spec, out):
    global ANIM; ANIM = 0.35
    b = Builder(spec, 1920); sc = b.scenes(); XF = 0.25
    total = sum(d for _, d in sc); n = int(total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x1920",
                           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
                           "-c:a", "aac", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    starts, acc = [], 0
    for _, d in sc: starts.append(acc); acc += d
    for f in range(n):
        t = f / FPS; i = max(k for k in range(len(sc)) if starts[k] <= t)
        fn, dur = sc[i]; lt = t - starts[i]; frame = fn(lt)
        if i + 1 < len(sc) and lt > dur - XF:
            frame = Image.blend(frame, sc[i + 1][0](0.0), (lt - (dur - XF)) / XF)
        frame = frame.convert("RGB"); ImageDraw.Draw(frame).rectangle([0, 0, int(W * t / total), 9], fill=SAGE)
        ff.stdin.write(frame.tobytes())
    ff.stdin.close(); ff.wait(); print("reel", out, round(total, 1), "s")


def render_stills(spec, outdir, H):
    os.makedirs(outdir, exist_ok=True); b = Builder(spec, H); paths = []
    for i, (fn, _) in enumerate(b.scenes()):
        p = os.path.join(outdir, f"slide_{i + 1}.jpg" if H != 1920 else f"preview_{i + 1}.png")
        fn(20.0).convert("RGB").save(p, quality=95); paths.append(p)
    print("\n".join(paths)); return paths


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8")); mode = sys.argv[2]; out = sys.argv[3]
    if mode == "reel": render_reel(spec, out)
    elif mode == "carousel": render_stills(spec, out, 1350)
    else: render_stills(spec, out, 1920)
