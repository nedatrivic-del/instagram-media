import random, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
F='/home/claude/instagram-media/template/fonts/'
LOGO_PATH='/home/claude/instagram-media/template/logo.jpg'
W,H=1080,1350; S=2
PAPER=(250,246,238); INK=(52,62,74); RED=(198,30,44); SAGE=(168,200,184); MARK=(150,198,172); SAGE_D=(110,150,130)
def cav(sz,w=500):
    f=ImageFont.truetype(F+'DancingScript%5Bwght%5D.ttf',sz*S)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
TEX=None
def _noise(rng,scale,amp):
    h,w=max(2,H*S//scale),max(2,W*S//scale)
    n=rng.normal(0,1,(h,w)).astype(np.float32)
    im=Image.fromarray(((n*40)+128).clip(0,255).astype('uint8')).resize((W*S,H*S),Image.BICUBIC)
    return (np.array(im,dtype=np.float32)-128)/40*amp
def paper(seed):
    """Drawing-pad paper with embossed tooth (relief)."""
    global TEX
    rng=np.random.default_rng(seed)
    h=_noise(rng,3,0.9)+_noise(rng,7,1.0)+_noise(rng,16,0.6)+_noise(rng,60,0.35)
    h=np.array(Image.fromarray(((h*30)+128).clip(0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2)),dtype=np.float32)
    TEX=(h-h.min())/(h.max()-h.min()+1e-6)        # 0 = valley, 1 = peak
    gy,gx=np.gradient(h)
    shade=-(gx+gy)*1.0                                  # light from top-left
    a=np.full((H*S,W*S,3),PAPER,dtype=np.float32)+shade[...,None]+(TEX[...,None]-0.5)*3
    img=Image.fromarray(a.clip(0,255).astype('uint8')).convert('RGBA')
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
def highlight(img,x0,y0,x1,y1,seed,col=(150,198,172),alpha=175):
    """Felt-marker strokes: 2-3 overlapping passes, darker ends/overlaps, pigment skips paper valleys."""
    r=random.Random(seed); hgt=y1-y0
    m=Image.new('L',img.size,0); acc=np.zeros((H*S,W*S),np.float32)
    passes=2 if hgt<70 else 3
    for k in range(passes):
        lay=Image.new('L',img.size,0); dl=ImageDraw.Draw(lay)
        top=y0+k*hgt/passes-hgt*0.18+r.uniform(-3,3); bot=top+hgt/passes+hgt*0.42
        xs=x0-12+r.uniform(-6,4); xe=x1+12+r.uniform(-4,8); tilt=r.uniform(-4,4)
        dl.polygon([(xs*S,(top+tilt)*S),(xe*S,(top-tilt)*S),((xe-3)*S,(bot-tilt)*S),((xs+3)*S,(bot+tilt)*S)],fill=150)
        # pressure blobs at start/end of the stroke
        for ex in (xs+6,xe-6): dl.ellipse([(ex-7)*S,top*S,(ex+7)*S,bot*S],fill=60)
        acc+=np.array(lay.filter(ImageFilter.GaussianBlur(0.8*S)),np.float32)
    acc=np.minimum(acc,255)
    # streaks along the stroke direction (felt tip lines)
    st=np.random.default_rng(seed).normal(0,1,(H*S,1)).astype(np.float32)
    st=np.array(Image.fromarray(((st*40)+128).clip(0,255).astype('uint8')).resize((W*S,H*S),Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.5)),np.float32)
    streak=0.85+(st-128)/40*0.12
    tooth=0.55+0.45*TEX**0.7 if TEX is not None else 1
    al=(acc/255*alpha*1.55*streak*tooth).clip(0,240).astype('uint8')
    c=Image.new('RGBA',img.size,col+(0,)); c.putalpha(Image.fromarray(al))
    return Image.alpha_composite(img,c)
strikes=[]
LOGO=None
def stamp_logo(img,x=95,yc=1225,w=470):
    """Multiply-blend the logo onto the paper so the paper texture shows through it."""
    global LOGO
    if LOGO is None:
        src=np.array(Image.open(LOGO_PATH).convert('RGB')).astype(np.float32)
        bg=np.median(src[:5].reshape(-1,3),0)
        d=np.abs(src-bg).max(2); ys,xs=np.where(d>12)
        src=src[max(0,ys.min()-4):ys.max()+5, max(0,xs.min()-4):xs.max()+5]
        LOGO=np.clip(src/bg,0,1)
    lw=int(w*S); lh=int(LOGO.shape[0]*lw/LOGO.shape[1])
    f=np.array(Image.fromarray((LOGO*255).astype('uint8')).resize((lw,lh),Image.LANCZOS)).astype(np.float32)/255
    a=np.array(img).astype(np.float32); X=int(x*S); Y=int(yc*S-lh/2)
    a[Y:Y+lh,X:X+lw,:3]*=f
    return Image.fromarray(a.clip(0,255).astype('uint8'),'RGBA')
def write(d,x,y,tokens,size,seed,maxw=900,lh=1.18,rot=0):
    """tokens: list of (text, mark) mark in None/'u'(red underline)/'r'(red text). Returns end y and list of underline spans"""
    r=random.Random(seed); f=cav(size); cx=x; spans=[]; strikes.clear()
    for word,mark in tokens:
        if word=='\n': cx=x; y+=size*lh; continue
        wlen=d.textlength(word+' ',font=f)/S
        if cx+d.textlength(word,font=f)/S>x+maxw: cx=x; y+=size*lh
        by=y+r.uniform(-2.5,2.5)
        if word=='✓':
            ck=[(cx+4,by+size*0.62),(cx+18,by+size*0.80),(cx+44,by+size*0.30)]
            wobble(d,ck,SAGE_D,5,seed+int(by),1.0); cx+=58; continue
        d.text((cx*S,by*S),word,font=f,fill=INK)
        if mark=='s':
            core=word.strip('„“\"…,.!?:'); off=d.textlength(word[:len(word)-len(word.lstrip('„“\"…'))],font=f)/S
            strikes.append((cx+off-6,cx+off+d.textlength(core,font=f)/S+6,by+size*0.66))
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
            elif re.match(r'^(\W*)~(.+?)~(\W*)$',w):
                m2=re.match(r'^(\W*)~(.+?)~(\W*)$',w); out.append((m2.group(1)+m2.group(2)+m2.group(3),'s'))
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
        f=cav(96,700); tw=d.textlength(title,font=f)/S
        img=highlight(img,90,y+18,90+tw,y+100,seed); d=ImageDraw.Draw(img)
        d.text((95*S,y*S),title,font=f,fill=INK); y+=170
    _,sp0=write(ImageDraw.Draw(Image.new('RGBA',(W*S,H*S))),95,y,T(body),70,seed+1)
    for i,(a,b,yy) in enumerate(merge_spans(sp0)):
        img=highlight(img,a-2,yy-52,b+2,yy-6,seed+30+i,MARK,175)
    d=ImageDraw.Draw(img)
    y,spans=write(d,95,y,T(body),70,seed+1)
    for i,(a,b,yy) in enumerate(strikes):
        wobble(d,[(a-2,yy+9),(b+4,yy-7)],RED,3.2,seed+70+i)
    if sign:
        f=cav(76,600); d.text((95*S,(y+40)*S),'Ihre Zahnärztin Altstadt',font=f,fill=INK)
        underline(d,95,95+d.textlength('Ihre Zahnärztin Altstadt',font=f)/S,y+125,seed+50,SAGE_D,3)
    # footer
    if arrow:
        wobble(d,[(820,1272),(960,1262)],RED,3.2,seed+60); wobble(d,[(960,1262),(935,1245)],RED,3.2,seed+61); wobble(d,[(960,1262),(938,1282)],RED,3.2,seed+62)
    d.text((219*S,1262*S),'@dentistry.oldtown',font=cav(46,500),fill=SAGE_D)
    img=stamp_logo(img)
    img.resize((W,H),Image.LANCZOS).convert('RGB').save(out,quality=93)
o=sys.argv[1]
page(1,4,'Mythos oder Fakt?',"Fast alle sagen:\n„Ein bisschen Zahnfleischbluten beim Putzen ist doch ganz ~normal.~“\n\nIch verrate Ihnen etwas …",1,o+'/brief_1.jpg')
page(2,4,None,"… es ist *nicht* *normal.*\n\n*Gesundes* *Zahnfleisch* *blutet* *nicht.*\n\nMeist steckt eine kleine Entzündung dahinter – ausgelöst durch Belag am Zahnfleischrand. Und die gute Nachricht kommt gleich …",2,o+'/brief_2.jpg')
page(3,4,'Was hilft?',"✓ Weiterputzen – *sanft*, nicht ~fest~.\n\n✓ Die Zwischenräume *jeden* *Abend* reinigen.\n\n✓ Regelmäßig zur Mundhygiene.\n\nUnd wenn es nicht besser wird …",3,o+'/brief_3.jpg')
page(4,4,None,"… blutet es länger als *1–2* *Wochen,* schauen wir uns das gemeinsam an.\n\nIn Ruhe, ohne Druck – und mit Zeit für Ihre Fragen.",4,o+'/brief_4.jpg',sign=True,arrow=False)
