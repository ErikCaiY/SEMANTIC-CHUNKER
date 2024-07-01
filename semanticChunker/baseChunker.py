from abc import ABC, abstractmethod

class BaseChunker(ABC):
    @abstractmethod
    def _invoke(self) -> str:...

    @abstractmethod
    def segment_pdf(self, document: str) -> str:...


