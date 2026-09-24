from PIL import ImageDraw
import random
def draw_flowchart(draw:ImageDraw.ImageDraw, box, description:str, color, seed:int):
 x,y,w,h=box; r=random.Random(seed); labels=['Start','Evaluate','Best result','Finish']; coords=[(x+w//2-85,y+10),(x+w//2-85,y+70),(x+w//2-85,y+130),(x+w//2-85,y+190)]
 for i,(bx,by) in enumerate(coords):
  draw.rounded_rectangle((bx,by,bx+170,by+40),radius=5,outline=color,width=2)
  draw.text((bx+17,by+10),labels[i],fill=color)
  if i<3: draw.line((bx+85,by+40,bx+85,by+67),fill=color,width=2); draw.polygon([(bx+80,by+62),(bx+90,by+62),(bx+85,by+68)],fill=color)
 draw.text((x+8,y+h-28),description[:80],fill=color)
