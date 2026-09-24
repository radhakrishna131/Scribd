from PIL import ImageFont
from app.handwriting.styles import HandwritingStyle
def load_font(style: HandwritingStyle, size: int): return ImageFont.truetype(style.font, size)
