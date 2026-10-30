import random, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
F='/home/claude/instagram-media/template/fonts/'
W,H=1080,1350; S=2
PAPER=(250,246,238); INK=(52,62,74); RED=(176,42,42); SAGE=(168,200,184); SAGE_D=(110,150,130)
def cav(sz,w=500):
    f=ImageFont.truetype(F+'Caveat%5Bwght%5D.ttf',sz*S)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def paper(seed):
    rng=np.random.default_rng(seed)
    a=np.full((H*S,W*S,3),PAPER,dtype=np.float32)
    n=rng.normal(0,3.2,(H*S//4,W*S//4)); n=np.array(Image.fromarray(((n+128)).clip(0,255).astype('uint8')).resize((W*S,H*S),Image.BICUBIC),dtype=np.float32)-128
    a+=n[...,None]
    img=Image.fromarray(a.clip(0,255).astype('uint8')).convert('RGBA')
    # faint vignette
    v=Image.new('L',(W*S,H*S),0); dv=ImageDraw.Draw(v); dv.ellipse([-W*S*0.2,-H*S*0.2,W*S*1.2,H*S*1.2],fill=255); v=v.filter(ImageFilter.GaussianBlur(160))
    dark=Image.new('RGBA',img.size,(120,105,85,0)); dark.putalpha(v.point(lambda x:int((255-x)*0.12)))
    return Image.alpha_composite(img,dark)
def wobble(d,pts,col,w,seed,jit=2.0):
    r=random.Random(seed)
    p=[(x+r.uniform(-jit,jit),y+r.uniform(-jit,jit)) for x,y in pts]
    d.line([(x*S,y*S) for x,y in p],fill=col,width=int(w*S),joint='curve')
def underline(d,x0,x1,y,seed,col=RED,w=4):
    r=random.Random(seed); n=24
    pts=[(x0+(x1-x0)*i/n, y+math.sin(i/n*math.pi*1.3+r.random())*3+r.uniform(-1,1)) for i in range(n+1)]
    wobble(d,pts,col,w,seed,0.6)
def highlight(img,x0,y0,x1,y1,seed,col=SAGE):
    lay=Image.new('RGBA',img.size,(0,0,0,0)); dl=ImageDraw.Draw(lay); r=random.Random(seed)
    for k in range(3):
        dy=r.uniform(-6,6)
        dl.polygon([((x0-10+r.uniform(-6,6))*S,(y0+dy+r.uniform(-4,4))*S),((x1+14+r.uniform(-6,6))*S,(y0+dy-6)*S),((x1+8)*S,(y1+dy+r.uniform(-4,4))*S),((x0-14)*S,(y1+dy+6)*S)],fill=col+(115,))
    lay=lay.filter(ImageFilter.GaussianBlur(2*S))
    return Image.alpha_composite(img,lay)
def write(d,x,y,tokens,size,seed,maxw=900,lh=1.18,rot=0):
    """tokens: list of (text, mark) mark in None/'u'(red underline)/'r'(red text). Returns end y and list of underline spans"""
    r=random.Random(seed); f=cav(size); cx=x; spans=[]
    for word,mark in tokens:
        if word=='\n': cx=x; y+=size*lh; continue
        wlen=d.textlength(word+' ',font=f)/S
        if cx+d.textlength(word,font=f)/S>x+maxw: cx=x; y+=size*lh
        by=y+r.uniform(-2.5,2.5)
        if word=='✓':
            ck=[(cx+4,by+size*0.62),(cx+18,by+size*0.80),(cx+44,by+size*0.30)]
            wobble(d,ck,SAGE_D,5,seed+int(by),1.0); cx+=58; continue
        d.text((cx*S,by*S),word,font=f,fill=RED if mark=='r' else INK)
        if mark=='u': core=word.strip('„“"…,.!?:'); off=d.textlength(word[:len(word)-len(word.lstrip('„“"…'))],font=f)/S; spans.append((cx+off,cx+off+d.textlength(core,font=f)/S,by+size*1.08))
        cx+=wlen
    return y+size*lh,spans
import re
def T(s):
    out=[]
    for line in s.split('\n'):
        for w in line.split(' '):
            if not w: continue
            m=re.match(r'^(\W*)\*(.+?)\*(\W*)$',w)
            if m: out.append((m.group(1)+m.group(2)+m.group(3),'u'))
            elif w.startswith('~'): out.append((w.strip('~'),'r'))
            else: out.append((w,None))
        out.append(('\n',None))
    return out[:-1]
def merge_spans(spans):
    spans=sorted(spans,key=lambda s:(int(s[2]//40),s[0])); out=[]
    for s in spans:
        if out and abs(out[-1][2]-s[2])<20 and s[0]-out[-1][1]<40: out[-1]=(min(out[-1][0],s[0]),max(out[-1][1],s[1]),out[-1][2])
        else: out.append(s)
    return out
def page(n,total,title,body,seed,out,sign=False,arrow=True):
    img=paper(seed); d=ImageDraw.Draw(img)
    dry=ImageDraw.Draw(Image.new('RGBA',(W*S,H*S)))
    hh=(170 if title else 0)+write(dry,95,0,T(body),70,seed+1)[0]+(160 if sign else 0)
    y=max(140,(1200-hh)/2)
    if title:
        f=cav(92,700); tw=d.textlength(title,font=f)/S
        img=highlight(img,90,y+18,90+tw,y+100,seed); d=ImageDraw.Draw(img)
        d.text((95*S,y*S),title,font=f,fill=INK); y+=170
    y,spans=write(d,95,y,T(body),70,seed+1)
    for i,(a,b,yy) in enumerate(merge_spans(spans)): underline(d,a-4,b+6,yy,seed+10+i)
    if sign:
        f=cav(70,600); d.text((95*S,(y+40)*S),'Ihre Zahnärztin Altstadt',font=f,fill=INK)
        underline(d,95,95+d.textlength('Ihre Zahnärztin Altstadt',font=f)/S,y+125,seed+50,SAGE_D,3)
    # footer
    d.text((95*S,1250*S),'@dentistry.oldtown',font=cav(38,500),fill=SAGE_D)
    if arrow:
        wobble(d,[(820,1272),(960,1262)],RED,4,seed+60); wobble(d,[(960,1262),(935,1245)],RED,4,seed+61); wobble(d,[(960,1262),(938,1282)],RED,4,seed+62)
    img.resize((W,H),Image.LANCZOS).convert('RGB').save(out,quality=93)
o=sys.argv[1]
page(1,4,'MYTHOS ODER FAKT?',"Fast alle sagen:\n„Ein bisschen Zahnfleischbluten beim Putzen ist doch ganz *normal.*“\n\nIch verrate Ihnen etwas …",1,o+'/brief_1.jpg')
page(2,4,None,"… es ist *nicht* normal.\n\n*Gesundes* *Zahnfleisch* *blutet* *nicht.*\n\nMeist steckt eine kleine Entzündung dahinter – ausgelöst durch Belag am Zahnfleischrand. Und die gute Nachricht kommt gleich …",2,o+'/brief_2.jpg')
page(3,4,'WAS HILFT?',"✓ Weiterputzen – *sanft*, nicht fest.\n\n✓ Die Zwischenräume *jeden* *Abend* reinigen.\n\n✓ Regelmäßig zur Mundhygiene.\n\nUnd wenn es nicht besser wird …",3,o+'/brief_3.jpg')
page(4,4,None,"… blutet es länger als *1–2* *Wochen,* schauen wir uns das gemeinsam an.\n\nIn Ruhe, ohne Druck – und mit Zeit für Ihre Fragen.",4,o+'/brief_4.jpg',sign=True,arrow=False)
