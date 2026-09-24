from dataclasses import dataclass,asdict
from pathlib import Path
from uuid import uuid4
import asyncio
from app.ai.service import NotesService
from app.handwriting.renderer import HandwritingRenderer
from app.pdf.generator import generate_pdf
ROOT=Path(__file__).resolve().parents[3]/'generated'
@dataclass
class Job:
 id:str; status:str='queued'; progress:int=0; current_step:str='Waiting to begin'; error:str|None=None; pages:list[str]|None=None; pdf_url:str|None=None
class JobStore:
 def __init__(self): self.jobs:dict[str,Job]={}
 def create(self):
  j=Job(id=uuid4().hex); self.jobs[j.id]=j; return j
 def get(self,id): return self.jobs.get(id)
store=JobStore()
async def run_topic(job:Job, topic:str, instruction:str, diagrams:bool, examples:bool, exam:bool):
 try:
  job.status='processing'; job.progress=12; job.current_step='Preparing content...'; await asyncio.sleep(.05)
  job.progress=30; job.current_step='Organizing notes...'; notes=await NotesService().generate(topic,instruction,diagrams,examples,exam)
  job.progress=55; job.current_step='Creating page layouts...'; directory=ROOT/job.id
  job.progress=70; job.current_step='Rendering handwriting...'; images=HandwritingRenderer().render(notes,directory)
  job.progress=88; job.current_step='Creating PDF...'; pdf=generate_pdf(images,directory/f'handwritten-notes-{job.id}.pdf')
  job.pages=[f'/generated/{job.id}/{p.name}' for p in images]; job.pdf_url=f'/api/generation/{job.id}/pdf'; job.status='completed'; job.progress=100; job.current_step='Done!'
 except Exception as exc: job.status='failed'; job.error=str(exc); job.current_step='Generation failed'
