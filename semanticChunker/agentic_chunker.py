from openai import OpenAI
import time
from .baseChunker import BaseChunker
from .PROMPT import EXAMPLE, QUERY_PROMPT, SYSTEM_PROMPT

class AgenticChunker_kimi(BaseChunker):
    def __init__(
            self, 
            kimi_api_key=None,
            model='moonshot-v1-128k', 
            base_url="https://api.moonshot.cn/v1", 
            temperature=0.3, 
            max_token=8192
            ):
        
        if kimi_api_key is None:
            raise ValueError("API key is not provided.")

        self.client = OpenAI(
            api_key = kimi_api_key,
            base_url = base_url,
        )
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_token

    def _invoke(self, document: str):
        completion = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f'{EXAMPLE}\n\n{QUERY_PROMPT}\n{document}'}
            ],
            temperature = self.temperature,
            max_tokens=self.max_tokens,
        )
        time.sleep(60)
        return completion.choices[0].message.content
    
    def segment_pdf(self, document: str) -> str:
        res = self._invoke(document=document)
        return res