from fastapi import APIRouter,BackgroundTasks,File,UploadFile,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from pypdf import PdfReader
from io import BytesIO
from app.services.jobs import store,run_topic,ROOT
from app.syllabus.parser import parse_syllabus
from app.youtube.transcript import is_valid_youtube_url,fetch_transcript
router=APIRouter(prefix='/api')
class TopicRequest(BaseModel):
 topic:str=Field(min_length=2,max_length=500); instruction:str=Field(default='',max_length=1000); include_diagrams:bool=False; include_examples:bool=False; exam_oriented:bool=True
class TextRequest(BaseModel): syllabus:str=Field(min_length=3,max_length=50000)
class YoutubeRequest(BaseModel): url:str=Field(min_length=8,max_length=500)
def start(request:TopicRequest,tasks:BackgroundTasks):
 job=store.create(); tasks.add_task(run_topic,job,request.topic,request.instruction,request.include_diagrams,request.include_examples,request.exam_oriented); return {'id':job.id,'status':job.status,'progress':job.progress,'current_step':job.current_step}
@router.get('/health')
def health(): return {'status':'ok'}
@router.post('/generate/topic')
def topic(request:TopicRequest,tasks:BackgroundTasks): return start(request,tasks)
@router.post('/generate/syllabus')
def syllabus(request:TextRequest,tasks:BackgroundTasks): return start(TopicRequest(topic='Study notes: '+ '; '.join(parse_syllabus(request.syllabus)),include_diagrams=True,include_examples=True),tasks)
@router.post('/parse/syllabus')
def parse(request:TextRequest): return {'topics':parse_syllabus(request.syllabus)}
@router.post('/generate/syllabus-pdf')
async def syllabus_pdf(tasks:BackgroundTasks,file:UploadFile=File(...)):
 if file.content_type not in {'application/pdf','application/x-pdf'}: raise HTTPException(400,detail={'error':{'code':'INVALID_FILE','message':'Please upload a PDF file.'}})
 data=await file.read()
 if len(data)>10*1024*1024: raise HTTPException(400,detail={'error':{'code':'FILE_TOO_LARGE','message':'PDF must be smaller than 10 MB.'}})
 try: text='\n'.join(p.extract_text() or '' for p in PdfReader(BytesIO(data)).pages)
 except Exception: text=''
 if len(text.strip())<30: raise HTTPException(400,detail={'error':{'code':'PDF_EXTRACTION_FAILED','message':"Couldn't extract enough text from this PDF. Please upload a clearer PDF or paste the syllabus manually."}})
 return syllabus(TextRequest(syllabus=text),tasks)
@router.post('/youtube/transcript')
async def transcript(request:YoutubeRequest): return {'transcript':await fetch_transcript(request.url)}
@router.post('/generate/youtube')
async def youtube(request:YoutubeRequest,tasks:BackgroundTasks):
 transcript=await fetch_transcript(request.url); return start(TopicRequest(topic='Lecture notes: '+transcript[:12000],include_diagrams=True,include_examples=True),tasks)
@router.get('/generation/{job_id}')
def generation(job_id:str):
 job=store.get(job_id)
 if not job: raise HTTPException(404,detail={'error':{'code':'NOT_FOUND','message':'Generation not found.'}})
 return job.__dict__
@router.get('/generation/{job_id}/pages')
def pages(job_id:str):
 job=store.get(job_id)
 if not job: raise HTTPException(404,detail='Not found')
 return {'pages':job.pages or []}
@router.get('/generation/{job_id}/pdf')
def pdf(job_id:str):
 path=ROOT/job_id/f'handwritten-notes-{job_id}.pdf'
 if not path.is_file(): raise HTTPException(404,detail='PDF is not ready')
 return FileResponse(path,media_type='application/pdf',filename='handwritten-notes.pdf')
