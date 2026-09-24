from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
def generate_pdf(images:list[Path], destination:Path)->Path:
 c=canvas.Canvas(str(destination),pagesize=A4); w,h=A4
 for image in images:
  c.drawImage(ImageReader(str(image)),0,0,width=w,height=h,preserveAspectRatio=True,mask='auto'); c.showPage()
 c.save(); return destination
