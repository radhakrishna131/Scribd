from PIL import ImageDraw, ImageFont
def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
 words=text.split(); lines=[]; line=''
 for word in words:
  trial=f'{line} {word}'.strip()
  if line and draw.textlength(trial,font=font)>width: lines.append(line); line=word
  else: line=trial
 if line: lines.append(line)
 return lines
