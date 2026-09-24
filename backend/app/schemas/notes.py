from enum import Enum
from pydantic import BaseModel, Field

class SectionType(str, Enum):
 definition='definition'; paragraph='paragraph'; heading='heading'; subheading='subheading'; bullet_list='bullet_list'; numbered_list='numbered_list'; steps='steps'; example='example'; formula='formula'; table='table'; diagram='diagram'; comparison='comparison'; key_points='key_points'; warning='warning'; conclusion='conclusion'
class NoteSection(BaseModel):
 type: SectionType
 heading: str | None = Field(default=None, max_length=120)
 content: str | None = Field(default=None, max_length=5000)
 items: list[str] = Field(default_factory=list, max_length=25)
 description: str | None = Field(default=None, max_length=1000)
class NotePage(BaseModel):
 page_title: str = Field(min_length=1, max_length=160)
 sections: list[NoteSection] = Field(min_length=1, max_length=30)
class StructuredNotes(BaseModel):
 document_title: str = Field(min_length=1, max_length=160)
 subject: str = Field(default='General Studies', max_length=100)
 level: str = Field(default='Undergraduate', max_length=100)
 pages: list[NotePage] = Field(min_length=1, max_length=30)
