import json, os
from app.ai.provider import AIProvider
from app.ai.prompts import STRUCTURED_NOTES_PROMPT
from app.schemas.notes import StructuredNotes
class GeminiProvider(AIProvider):
 async def generate_notes(self, topic, instruction, diagrams, examples, exam_oriented):
  from google import genai
  client=genai.Client(api_key=os.environ['GEMINI_API_KEY'])
  prompt=f'{STRUCTURED_NOTES_PROMPT}\nTopic: {topic}\nInstruction: {instruction}\nInclude diagrams: {diagrams}; examples: {examples}; exam oriented: {exam_oriented}'
  response=client.models.generate_content(model='gemini-2.0-flash', contents=prompt, config={'response_mime_type':'application/json'})
  return StructuredNotes.model_validate(json.loads(response.text))
