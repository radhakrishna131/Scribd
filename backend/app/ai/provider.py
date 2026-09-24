from abc import ABC, abstractmethod
from app.schemas.notes import StructuredNotes
class AIProvider(ABC):
 @abstractmethod
 async def generate_notes(self, topic: str, instruction: str, diagrams: bool, examples: bool, exam_oriented: bool) -> StructuredNotes: ...
