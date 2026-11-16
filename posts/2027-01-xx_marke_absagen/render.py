# Carousel "Es ist doch nur ein Termin" – same photo on every slide, quote on the wall (idea: viral cancellation-policy carousel)
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..'); F=os.path.join(ROOT,'template','fonts')
W,H=1080,1350; INK=(55,64,76); RED=(166,41,41); SOFT=(96,106,118)
def osw(sz,w=300):
    f=ImageFont.truetype(os.path.join(F,'Oswald%5Bwght%5D.ttf'),sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def fira(sz,st='Light'): return ImageFont.truetype(os.path.join(F,f'FiraSans-{st}.ttf'),sz)
def wrap(d,t,f,mw):
    out=[];cur=''
    for w in t.split():
        x=(cur+' '+w).strip()
        if d.textlength(x,font=f)<=mw: cur=x
        else: out.append(cur);cur=w
    out.append(cur);return out
src=Image.open(sys.argv[1]).convert('RGB').crop((0,0,1080,1350))
src=ImageEnhance.Color(src).enhance(0.55); src=ImageEnhance.Contrast(src).enhance(0.95)
lg=Image.open(os.path.join(ROOT,'template','logo.png')).convert('RGBA'); logo=lg.resize((320,int(lg.height*320/lg.width)),Image.LANCZOS)
S=[
 dict(q='„Die Zahnärztin hat mir den Termin verrechnet – nur weil ich ihn vergessen habe.“',sub=None,well='Nun ja …'),
 dict(q='„Ich habe den Zug verpasst.“',sub='Das Ticket ist trotzdem weg …'),
 dict(q='„Ich habe das Konzert vergessen.“',sub='Die Karte bekomme ich nicht zurück …'),
 dict(q='„Ich habe vergessen, das Abo zu kündigen.“',sub='Abgebucht wurde trotzdem …'),
 dict(q='„Es ist doch nur ein Termin.“',sub='Für uns ist es eine Stunde, die nur für Sie reserviert war – und die jemand mit Zahnschmerzen gut gebraucht hätte.'),
 dict(q='Absagen ist ganz einfach.',sub='Bis 24 Stunden vorher – telefonisch oder online. Kostenlos. Wir erinnern Sie 48 Stunden vorher per SMS.',cta=True),
]
out=sys.argv[2]
for i,s in enumerate(S,1):
    img=src.copy().convert('RGBA')
    # soften the wall area so text reads calmly
    veil=Image.new('RGBA',(W,H),(0,0,0,0)); vd=ImageDraw.Draw(veil)
    for y in range(0,760): vd.line([(0,y),(W,y)],fill=(250,247,240,int(185*(1-y/760)**1.1)))
    img.alpha_composite(veil); d=ImageDraw.Draw(img)
    qf=osw(76 if len(s['q'])<40 else 64,300); CX=470; MW=800; lines=wrap(d,s['q'].upper(),qf,MW)
    y=150; lh=int(qf.size*1.2)
    for ln in lines:
        d.text((CX-d.textlength(ln,font=qf)/2,y),ln,font=qf,fill=INK); y+=lh
    if s.get('sub'):
        y+=28; sf=fira(38,'Light'); 
        for ln in wrap(d,s['sub'],sf,MW):
            d.text((CX-d.textlength(ln,font=sf)/2,y),ln,font=sf,fill=SOFT); y+=54
    if s.get('well'):
        wf=fira(64,'LightItalic'); d.text((W-110-d.textlength(s['well'],font=wf),1095),s['well'],font=wf,fill=INK)
    if s.get('cta'):
        y+=26; hf=fira(44,'Regular'); h='♡'
        pf=fira(32,'Regular'); txt='termine.softdent.at/zahnaerztin-altstadt'; tw=d.textlength(txt,font=pf)
        d.rounded_rectangle([CX-tw/2-34,y,CX+tw/2+34,y+70],radius=35,fill=INK+(235,))
        d.text((CX-tw/2,y+15),txt,font=pf,fill=(255,255,255))
    # footer: logo + handle bottom-left on a soft cream strip
    strip=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(strip).rectangle([0,H-150,W,H],fill=(250,247,240,215))
    img.alpha_composite(strip.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(logo,(W-64-logo.width,H-75-logo.height//2)); d=ImageDraw.Draw(img)
    d.text((64,H-96),'@dentistry.oldtown',font=fira(34,'Light'),fill=INK)
    
    img.convert('RGB').save(os.path.join(out,f'v1_slide_{i}.jpg'),quality=92)
print('ok')
