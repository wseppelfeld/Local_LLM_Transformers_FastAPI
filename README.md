# API FastAPI para Inferência com LLMs Locais (exemplo: Gemma-3-12B-IT)

Este projeto fornece uma API HTTP baseada em FastAPI para rodar inferência com modelos LLM locais (exemplo: Gemma-3-12B-IT do Hugging Face). Atualmente, o projeto está configurado para rodar inteiramente na CPU, garantindo estabilidade mesmo em máquinas sem GPU ou com pouca VRAM.

## Requisitos
- Python 3.8+
- pip
- [transformers](https://huggingface.co/docs/transformers/index)
- [fastapi](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [git-lfs](https://git-lfs.github.com/) (para baixar o modelo)

## Instalação
```bash
pip install fastapi uvicorn transformers
```

## Baixando o modelo (exemplo: Gemma-3-12B-IT)

1. **Configure sua conta Hugging Face e chaves SSH:**
   - Crie uma conta em https://huggingface.co/join se ainda não tiver.
   - Gere um token de acesso em https://huggingface.co/settings/tokens (leitura).
   - Instale o CLI do Hugging Face:
     ```bash
     pip install huggingface_hub
     ```
   - Faça login:
     ```bash
     huggingface-cli login
     ```
   - (Opcional, para SSH) Gere e adicione sua chave pública em https://huggingface.co/settings/keys

2. **Baixe o modelo:**
   ```bash
   git lfs install
   git clone https://huggingface.co/google/gemma-3-12b-it
   # Ou, para SSH:
   git clone git@hf.co:google/gemma-3-12b-it
   ```
   Isso criará a pasta `gemma-3-12b-it` no seu projeto.

## Como trocar o modelo utilizado

Para usar outro modelo, basta:
1. Baixar a pasta do modelo desejado do Hugging Face (como acima).
2. Alterar a variável `MODEL_DIR` no arquivo `api.py` para o caminho da nova pasta do modelo, por exemplo:
   ```python
   MODEL_DIR = "./nome-da-pasta-do-novo-modelo"
   ```
3. Certifique-se de que o modelo é compatível com a classe usada (`AutoModelForImageTextToText` ou outra adequada).

## Executando a API

1. Inicie o servidor:
   ```bash
   uvicorn api:app --reload
   ```
   Se a porta 8000 estiver ocupada, use `--port 8001` ou outra porta.

2. Teste a API:
   - Com curl:
     ```bash
     curl -X POST "http://127.0.0.1:8000/generate/" \
       -H "Content-Type: application/json" \
       -d '{"prompt": "Olá, como vai?"}'
     ```
   - Ou acesse http://127.0.0.1:8000/docs para a interface Swagger.

## Notas importantes
- O modelo roda inteiramente na CPU por padrão, garantindo estabilidade mesmo em máquinas sem GPU.
- Para melhor desempenho, utilize uma máquina com bastante RAM (mínimo recomendado: 32GB para modelos grandes).
- Se ocorrer erro de falta de memória (OOM), tente:
  - Reduzir `max_new_tokens` em `api.py` (ex: para 32 ou 64)
  - Fechar outros processos que usam muita RAM
  - Reiniciar o servidor
- Se o erro persistir, considere usar um modelo menor (ex: Gemma-2B, Llama-2-7B, etc).
- Os comentários do código estão em português.

## Licença
Este projeto é para uso pessoal e de pesquisa. Verifique a licença do modelo no Hugging Face para restrições de uso.
