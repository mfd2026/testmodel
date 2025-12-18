from typing import Any, Dict
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

WEIGHTS_DIR = "./weights"  # داخل الصورة


class Model:
    def __init__(self):
        # تحميل الـ tokenizer و الموديل من مجلد الأوزان داخل الصورة
        self.tokenizer = AutoTokenizer.from_pretrained(WEIGHTS_DIR)
        self.model = AutoModelForSequenceClassification.from_pretrained(WEIGHTS_DIR)
        self.model.eval()

        # نحاول أخذ id2label من config لو موجود
        id2label = getattr(self.model.config, "id2label", None)
        if id2label:
            # يكون dict بمفاتيح نصية، نحوله لـ int
            self.id2label = {int(k): v for k, v in id2label.items()}
        else:
            # fallback لو ما فيه config
            self.id2label = {1: "Human", 0: "AI"}

    @torch.inference_mode()
    def predict(self, text: str) -> Dict[str, Any]:
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt",
        )

        outputs = self.model(**inputs)
        logits = outputs.logits  # [1, num_labels]
        probs_tensor = F.softmax(logits, dim=-1)[0]
        probs = probs_tensor.tolist()
        pred_id = int(torch.argmax(logits, dim=-1).item())
        pred_label = self.id2label.get(pred_id, str(pred_id))

        # نبني map اسم_اللابل -> probability
        probs_by_label = {
            self.id2label.get(i, str(i)): float(p)
            for i, p in enumerate(probs)
        }

        return {
            "ok": True,
            "label": pred_label,
            "confidence": float(probs_by_label.get(pred_label, 0.0)),
            "probs": probs_by_label,
        }


_model_instance: Model | None = None


def get_model() -> Model:
    global _model_instance
    if _model_instance is None:
        _model_instance = Model()
    return _model_instance
