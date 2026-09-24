from dataclasses import dataclass
@dataclass(frozen=True)
class HandwritingStyle:
 name:str='blue_ballpoint'; font:str='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; pen_color:tuple=(20,73,142); font_size:int=27; line_height:int=43; letter_spacing:float=.2; baseline_variation:float=1.2; rotation_variation:float=.35; stroke_variation:float=.2
@dataclass(frozen=True)
class PaperStyle:
 name:str='plain'; background:tuple=(255,253,247); line_spacing:int=50; margin:int=105
BLUE_BALLPOINT=HandwritingStyle(); PAPER_STYLES={'plain':PaperStyle(), 'ruled':PaperStyle(name='ruled'), 'grid':PaperStyle(name='grid')}
