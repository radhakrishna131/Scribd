import os
from app.schemas.notes import StructuredNotes, NotePage, NoteSection
from app.ai.gemini import GeminiProvider

def fallback_notes(topic: str, instruction: str, diagrams: bool, examples: bool, exam: bool) -> StructuredNotes:
 title=topic.strip().rstrip('?')
 sections=[NoteSection(type='definition',heading='Definition',content=f'{title} is an important concept studied to make informed, systematic decisions. It describes a method for evaluating choices using available information.'),NoteSection(type='paragraph',heading='Core idea',content=f'The central aim is to solve the problem efficiently while maintaining correctness. Start from the initial situation, examine valid alternatives, and retain the best outcome found so far.'),NoteSection(type='steps',heading='Method',items=['State the problem, objective, and constraints clearly.','Evaluate the next available choice using the relevant criterion.','Update the current best result when a better choice is found.','Stop when no remaining choice can improve the answer.']),NoteSection(type='key_points',heading='Exam points',items=['Define the concept before explaining the procedure.','Mention correctness, efficiency, and a practical use case.','Use a labelled diagram to support the answer.'])]
 if examples: sections.append(NoteSection(type='example',heading='Example',content=f'Consider a small decision tree for {title}. Evaluate the first branch, record its value, then avoid later branches once they cannot beat the recorded result.'))
 if diagrams: sections.append(NoteSection(type='diagram',heading='Concept diagram',description=f'A simple flowchart showing Start, evaluate alternatives for {title}, retain best result, and finish.'))
 sections.append(NoteSection(type='conclusion',heading='Conclusion',content=f'In summary, {title} provides a structured way to reach a reliable answer with less unnecessary work.'))
 return StructuredNotes(document_title=title,subject='Computer Science',level='Undergraduate',pages=[NotePage(page_title=title,sections=sections)])

class NotesService:
 async def generate(self, topic, instruction='', diagrams=False, examples=False, exam_oriented=True):
  if os.getenv('GEMINI_API_KEY'):
   try: return await GeminiProvider().generate_notes(topic,instruction,diagrams,examples,exam_oriented)
   except Exception: pass
  return fallback_notes(topic,instruction,diagrams,examples,exam_oriented)
