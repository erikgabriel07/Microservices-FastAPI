# Imagem oficial do python como base
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /fastapi-application

# Copiando arquivo de requisitos para o diretório de trabalho
COPY ./requirements.txt .

# Instação de dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiando código da aplicação para o diretório de trabalho
COPY . .

# Expondo serviço na porta 8000
EXPOSE 8000

# Executando aplicação
CMD ["python", "FastAPI/main.py"]
