import sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/home/claude/instagram-media/template/fonts/"
RED=(150,36,36); SLATE=(71,82,95); CREAM=(247,243,234); SAGE=(169,202,187)
W,H=1080,1350; X=80; MAXW=W-2*X
def osw(s,w=600):
    f=ImageFont.truetype(F+"Oswald%5Bwght%5D.ttf",s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def fira(s,st="Light"): return ImageFont.truetype(F+f"FiraSans-{st}.ttf",s)
def paper():
    bg=Image.new("RGB",(W,H),CREAM)
    n=Image.effect_noise((W,H),18).convert("L").point(lambda v:128+(v-128)//4).filter(ImageFilter.GaussianBlur(0.6))
    return Image.blend(bg,Image.merge("RGB",(n,n,n)),0.06)
def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        c=(cur+" "+w).strip()
        if d.textlength(c,font=f)<=mw: cur=c
        else: out.append(cur);cur=w
    out.append(cur);return out
def spaced(d,xy,t,f,fill,sp=6,right=False):
    tw=sum(d.textlength(ch,font=f)+sp for ch in t)-sp
    x,y=xy
    if right: x-=tw
    for ch in t: d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+sp
spec=json.load(open(sys.argv[1])); n=len(spec)
for i,s in enumerate(spec):
    img=paper(); d=ImageDraw.Draw(img)
    spaced(d,(X,70),"ZAHNÄRZTIN ALTSTADT",fira(24,"Regular"),SLATE)
    spaced(d,(W-X,70),f"{i+1:02d} / {n:02d}",fira(24,"Regular"),SLATE,right=True)
    y=190; hf=osw(s.get("size",140))
    for line in s["head"]:
        for l in wrap(d,line.upper(),hf,MAXW):
            d.text((X,y),l,font=hf,fill=RED); y+=int(hf.size*1.08)
    y+=75; bf=fira(s.get("bsize",50))
    for p in s.get("body",[]):
        if p=="": y+=24; continue
        for l in wrap(d,p,bf,MAXW):
            d.text((X,y),l,font=bf,fill=SLATE); y+=int(bf.size*1.38)
        y+=14
    if s.get("tag"):
        y+=30; tf=osw(62,500)
        for l in wrap(d,s["tag"].upper(),tf,MAXW): d.text((X,y),l,font=tf,fill=RED); y+=int(tf.size*1.12)
    if s.get("card"):
        cy=H-330; d.rounded_rectangle([X,cy,W-X,cy+210],radius=28,fill=RED)
        d.text((X+50,cy+38),"KAPITELGASSE 9 · SALZBURGER ALTSTADT",font=osw(44,500),fill=CREAM)
        d.text((X+50,cy+110),"Alle Kassen & Privat · Termine online – Link in der Bio",font=fira(30,"Regular"),fill=CREAM)
    if y>H-120: print("OVERFLOW slide",i+1,y)
    if i<n-1: d.line([(W-X-150,H-95),(W-X,H-95)],fill=SLATE,width=3); d.line([(W-X-18,H-107),(W-X,H-95),(W-X-18,H-83)],fill=SLATE,width=3)
    else: d.text((X,H-110),"@dentistry.oldtown",font=fira(28,"Regular"),fill=SLATE)
    img.save(f"{sys.argv[2]}/slide_{i+1}.jpg",quality=94)
