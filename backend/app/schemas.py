from pydantic import BaseModel

class ClassifyRequest(BaseModel):
  text: str

class ClassifyResponse(BaseModel):
  category: str # "Produtivo" | "Improdutivo"
  probability: float
  reply: str