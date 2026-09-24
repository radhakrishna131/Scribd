from app.schemas.notes import NoteSection
def section_text(section: NoteSection) -> list[str]:
 if section.items: return [f'{i+1}) {item}' if section.type in ('steps','numbered_list') else f'• {item}' for i,item in enumerate(section.items)]
 return [section.content or section.description or '']
