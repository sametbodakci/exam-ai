from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import io
import os

# .env dosyasını yükle
load_dotenv()

# FastAPI uygulaması
app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Backend çalışıyor 🚀"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """PDF dosyası yükleme ve AI ile soru üretimi"""
    if not file.filename.endswith(".pdf"):
        return {"error": "Sadece PDF dosyaları destekleniyor."}

    try:
        content = await file.read()
        text = extract_text_from_pdf(content)

        # AI'ye gönderilecek prompt
        prompt = f"""
        Aşağıdaki PDF içeriğine göre 5 anlamlı, açık uçlu sınav sorusu oluştur:
        ---
        {text[:4000]}
        ---
        """

        # OpenAI'den yanıt al
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen bir sınav sorusu oluşturma asistanısın."},
                {"role": "user", "content": prompt}
            ],
        )

        questions_text = response.choices[0].message.content
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
        return {"predictions": questions}

    except Exception as e:
        return {"error": str(e)}

def extract_text_from_pdf(pdf_bytes):
    """PDF içeriğini metne çevir"""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

