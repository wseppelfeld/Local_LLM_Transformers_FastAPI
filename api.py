
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoProcessor, AutoModelForImageTextToText

app = FastAPI()


# Carrega o modelo e o processador uma vez ao iniciar
MODEL_DIR = "./gemma-3-12b-it"

processor = AutoProcessor.from_pretrained(MODEL_DIR)

# Tenta carregar na GPU primeiro, se falhar usa CPU
try:
    if torch.cuda.is_available():
        model = AutoModelForImageTextToText.from_pretrained(
            MODEL_DIR,
            device_map="cpu",  # Força CPU para evitar erros de assert CUDA
            torch_dtype=torch.float32,  # Usa float32 para estabilidade
            low_cpu_mem_usage=True
        )
        MODEL_DEVICE = "cpu"
    else:
        model = AutoModelForImageTextToText.from_pretrained(
            MODEL_DIR,
            device_map="cpu",
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        MODEL_DEVICE = "cpu"
except Exception as e:
    model = AutoModelForImageTextToText.from_pretrained(
        MODEL_DIR,
        device_map="cpu",
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    MODEL_DEVICE = "cpu"

class GenerateRequest(BaseModel):
    prompt: str


@app.post("/generate/")
async def generate_text(request: GenerateRequest):
    # Prepara mensagens para prompt somente de texto
    messages = [
        {"role": "user", "content": [{"type": "text", "text": request.prompt}]}
    ]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    # Usa sempre CPU para evitar erros CUDA de device-side assert
    device = torch.device("cpu")
    inputs = {k: v.to(device, dtype=torch.long if k in ['input_ids', 'attention_mask'] else torch.float32) 
              if hasattr(v, 'to') else v for k, v in inputs.items()}
    
    outputs = model.generate(**inputs, max_new_tokens=128)
    response = processor.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
    return {"response": response}


