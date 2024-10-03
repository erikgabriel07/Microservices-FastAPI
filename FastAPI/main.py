from fastapi import FastAPI
from routes import init_routes
from uvicorn import run as startapp


def main():
    app = FastAPI(debug=True) # debug somente em desenvolvimento
    init_routes(app)
    
    startapp(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()

# Alteração feita abaixo por Valter Junior

from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

# Defina o diretório onde os arquivos estão localizados
DIRETORIO_ARQUIVOS = "./arquivos"


@app.get("/arquivos/")
async def listar_arquivos():
    try:
        # Listar arquivos no diretório especificado
        arquivos = os.listdir(DIRETORIO_ARQUIVOS)
        # Filtrar apenas arquivos (ignorando subdiretórios)
        arquivos = [f for f in arquivos if os.path.isfile(os.path.join(DIRETORIO_ARQUIVOS, f))]
        return {"arquivos": arquivos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/processar/")
async def processar_arquivos(arquivo: str):
    # Verifique se o arquivo existe
    caminho_arquivo = os.path.join(DIRETORIO_ARQUIVOS, arquivo)
    if not os.path.isfile(caminho_arquivo):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    # Aqui você pode aplicar a lógica de processamento que deseja
    # Por exemplo, vamos apenas retornar o tamanho do arquivo
    tamanho = os.path.getsize(caminho_arquivo)

    return {"arquivo": arquivo, "tamanho": tamanho}
