from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .config import settings
from .schemas import ClassifyResponse
from .model import EmailClassifier
from .utils import extract_text_from_pdf
import os

from openai import OpenAI, RateLimitError, AuthenticationError

app = FastAPI(title="Email Classifier API")

app.add_middleware(
  CORSMiddleware,
  allow_origins=[o.strip() for o in settings.allow_origins.split(",")],
  allow_methods=["*"],
  allow_headers=["*"],
)

_model = EmailClassifier.load(settings.model_path) if os.path.exists(settings.model_path) else None

class Error(BaseModel):
  detail: str


class ReplyGenerator:
  def __init__(self, api_key: str | None = None):
    self.api_key = api_key
    self.client = OpenAI(api_key=api_key) if api_key else None

  async def generate(self, category: str, email_text: str) -> str:
    if not self.client:
      return self._mock_reply(category, email_text, "API Key ausente")

    try:
      system = (
        "Você é um assistente de atendimento bancário. Seja objetivo, gentil e claro."
        " Se o email for Improdutivo (cumprimentos/agradecimentos), responda cordialmente"
        " sem abrir ticket, em 2-3 linhas. Se for Produtivo, peça dados mínimos (ID da"
        " requisição, CPF/CNPJ mascarado, etc.) e diga o próximo passo. Nunca prometa"
        " prazos específicos. Responda em português do Brasil."
      )

      user = f"Categoria: {category}\n---\nEmail recebido:\n{email_text[:2000]}"

      completion = self.client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
          {"role": "system", "content": system},
          {"role": "user", "content": user},
        ],
      )
      return completion.choices[0].message.content.strip()

    except (RateLimitError, AuthenticationError) as e:
      return self._mock_reply(category, email_text, str(e))
    except Exception as e:
      return self._mock_reply(category, email_text, f"Erro inesperado: {str(e)}")

  def _mock_reply(self, category: str, email_text: str, reason: str) -> str:
    if "insufficient_quota" in reason or "429" in reason:
      reason = "Quota da API esgotada"
    elif "API Key" in reason:
      reason = "API Key ausente ou inválida"
    else:
      reason = "Falha ao acessar a API"

    return (
      f"[MOCK] Resposta simulada para categoria '{category}'. "
      f"Trecho do conteúdo: '{email_text[:50]}...'. "
      f"Motivo: {reason}"
    )


reply_generator = ReplyGenerator(api_key=settings.openai_api_key)


@app.post("/api/classify", response_model=ClassifyResponse, responses={400: {"model": Error}})
async def classify(
  text: str | None = Form(default=None),
  file: UploadFile | None = File(default=None),
):
  if not text and not file:
    return JSONResponse(status_code=400, content={"detail": "Envie 'text' ou 'file'"})

  content = text or ""
  if file:
    data = await file.read()
    if file.content_type == "application/pdf":
      content = extract_text_from_pdf(data)
    else:
      content = data.decode("utf-8", errors="ignore")

  if not content.strip():
    return JSONResponse(status_code=400, content={"detail": "Arquivo/texto vazio"})

  if _model is None:
    return JSONResponse(status_code=500, content={"detail": "Modelo não carregado"})

  labels, probs = _model.predict_proba_label([content])
  category = labels[0]
  probability = probs[0]

  reply = await reply_generator.generate(category, content)

  return ClassifyResponse(category=category, probability=probability, reply=reply)


@app.post("/api/reply")
async def regenerate_reply(
  category: str = Body(...),
  text: str = Body(...)
):
  reply = await reply_generator.generate(category, text)
  return {"reply": reply}
