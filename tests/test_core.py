import asyncio
from pathlib import Path
from app.ai.service import NotesService
from app.handwriting.layout import wrap_text
from app.handwriting.pagination import paginate
from app.handwriting.renderer import HandwritingRenderer
from app.pdf.generator import generate_pdf
from app.syllabus.parser import parse_syllabus
from app.youtube.transcript import is_valid_youtube_url
from PIL import Image,ImageDraw,ImageFont

def test_syllabus_parser(): assert parse_syllabus('Unit 1:\nAI\n Intelligent Agents\n')==['Intelligent Agents']
def test_youtube_validation(): assert is_valid_youtube_url('https://www.youtube.com/watch?v=abcdefghijk') and not is_valid_youtube_url('https://example.com/x')
def test_wrapping_respects_width():
 d=ImageDraw.Draw(Image.new('RGB',(500,500))); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20); lines=wrap_text(d,'The quick brown fox jumps over the lazy dog',f,130); assert len(lines)>1 and all(d.textlength(x,font=f)<=130 for x in lines)
def test_pagination_no_overflow():
 places=paginate([100,100,100],300,30,30); assert all(p.y+p.height<=270 for p in places)
def test_e2e_render_and_pdf(tmp_path:Path):
 notes=asyncio.run(NotesService().generate("Explain Dijkstra's Algorithm",'include diagram',True,True,True)); pages=HandwritingRenderer().render(notes,tmp_path); pdf=generate_pdf(pages,tmp_path/'notes.pdf'); assert pages and pdf.exists() and pdf.stat().st_size>100
