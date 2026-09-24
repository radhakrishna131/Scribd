from pathlib import Path
import random
from PIL import Image, ImageDraw
from app.schemas.notes import StructuredNotes, NoteSection
from app.handwriting.styles import BLUE_BALLPOINT, PAPER_STYLES
from app.handwriting.fonts import load_font
from app.handwriting.layout import wrap_text
from app.handwriting.elements import section_text
from app.handwriting.diagrams import draw_flowchart

W,H=1240,1754
class HandwritingRenderer:
 def __init__(self, paper='plain'): self.style=BLUE_BALLPOINT; self.paper=PAPER_STYLES.get(paper,PAPER_STYLES['plain'])
 def render(self, notes:StructuredNotes, out_dir:Path)->list[Path]:
  out_dir.mkdir(parents=True,exist_ok=True); pages=[]; page_no=0; image=None; draw=None; y=0
  body=load_font(self.style,self.style.font_size); heading=load_font(self.style,35); title=load_font(self.style,46)
  def new_page():
   nonlocal image,draw,y,page_no
   page_no+=1; image=Image.new('RGB',(W,H),self.paper.background); draw=ImageDraw.Draw(image)
   if self.paper.name in ('ruled','grid'):
    for yy in range(160,H-90,self.paper.line_spacing): draw.line((85,yy,W-85,yy),fill=(220,229,235),width=1)
    if self.paper.name=='grid':
     for xx in range(85,W-85,self.paper.line_spacing): draw.line((xx,100,xx,H-90),fill=(235,239,242),width=1)
   draw.line((85,95,85,H-90),fill=(245,186,186),width=2); y=125
  def save():
   draw.text((W-135,H-72),str(page_no),font=body,fill=self.style.pen_color)
   path=out_dir/f'page-{page_no}.png'; image.save(path,quality=95); pages.append(path)
  def ensure(height):
   nonlocal y
   if y+height>H-115:
    save(); new_page()
  new_page()
  for note_page in notes.pages:
   ensure(105); draw.text((110,y),note_page.page_title,font=title,fill=self.style.pen_color); y+=62; draw.line((110,y,W-125,y+2),fill=self.style.pen_color,width=2); y+=32
   for s in note_page.sections:
    if s.type=='diagram':
     ensure(290); draw.text((110,y),s.heading or 'Diagram',font=heading,fill=self.style.pen_color); y+=52; draw_flowchart(draw,(135,y,900,240),s.description or '',self.style.pen_color,hash(notes.document_title)); y+=255; continue
    lines=[]
    for text in section_text(s): lines.extend(wrap_text(draw,text,body,W-230))
    block_h=(48 if s.heading else 0)+max(1,len(lines))*self.style.line_height+24
    ensure(block_h)
    if s.heading: draw.text((110,y),s.heading,font=heading,fill=self.style.pen_color); y+=48
    for line in lines:
     jitter=random.Random(f'{page_no}{y}{line}').uniform(-1,1)
     draw.text((112+jitter,y+jitter),line,font=body,fill=self.style.pen_color,stroke_width=0); y+=self.style.line_height
    y+=20
  save(); return pages
