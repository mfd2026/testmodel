from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from .model_utils import get_model

app = FastAPI(title="testmodel API", version="0.5.0")


class Inp(BaseModel):
    text: str


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(inp: Inp):
    model = get_model()
    return model.predict(inp.text)


# static اختياري
if os.path.isdir("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home_page():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<title>testmodel • تصنيف النص</title>
<style>
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;max-width:820px;margin:40px auto;padding:0 16px}
  h1{font-size:20px;margin-bottom:10px}
  textarea{width:100%;min-height:140px;padding:10px;font-size:16px}
  button{padding:10px 16px;font-size:16px;cursor:pointer;margin-top:10px}
  .result{margin-top:16px;padding:12px;border:1px solid #ddd;border-radius:10px;background:#fafafa;white-space:pre-wrap;direction:ltr}
  .row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
</style>
</head>
<body>
  <h1>تصنيف النص (Human / AI)</h1>
  <p>اكتب النص ثم اضغط “تنبؤ”:</p>
  <textarea id="txt" placeholder="اكتب النص هنا..."></textarea>
  <div class="row">
    <button id="btn">تنبؤ</button>
    <span id="status"></span>
  </div>
  <div class="result" id="out"></div>

<script>
const btn = document.getElementById('btn');
const out = document.getElementById('out');
const st  = document.getElementById('status');
const tx  = document.getElementById('txt');

btn.onclick = async () => {
  const text = tx.value.trim();
  if (!text) { out.textContent = "الرجاء إدخال نص."; return; }
  st.textContent = "جارٍ التنبؤ ...";
  out.textContent = "";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({text})
    });
    const data = await res.json();
    st.textContent = "";
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    st.textContent = "";
    out.textContent = "حدث خطأ في الطلب: " + e;
  }
};
</script>
</body>
</html>
    """
