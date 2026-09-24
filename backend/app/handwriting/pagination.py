from dataclasses import dataclass
@dataclass
class BlockPlacement: page:int; y:int; height:int
def paginate(heights:list[int], page_height:int, top:int, bottom:int, gap:int=20)->list[BlockPlacement]:
 page=0; y=top; result=[]
 for height in heights:
  if y+height>page_height-bottom and y>top: page+=1; y=top
  result.append(BlockPlacement(page,y,height)); y+=height+gap
 return result
