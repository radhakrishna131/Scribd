import re
from urllib.parse import urlparse,parse_qs
def video_id(url:str)->str|None:
 p=urlparse(url)
 if p.netloc in {'youtu.be','www.youtu.be'}: return p.path.strip('/') or None
 if p.netloc.endswith('youtube.com'): return parse_qs(p.query).get('v',[None])[0]
 return None
def is_valid_youtube_url(url:str)->bool: return bool(video_id(url))
async def fetch_transcript(url:str)->str:
 vid=video_id(url)
 if not vid: raise ValueError('Please provide a valid YouTube URL.')
 try:
  from youtube_transcript_api import YouTubeTranscriptApi
  rows=YouTubeTranscriptApi().fetch(vid)
  return ' '.join(row.text for row in rows)
 except Exception as exc: raise ValueError("We couldn't retrieve a transcript for this video. Try another video or paste the lecture text manually.") from exc
