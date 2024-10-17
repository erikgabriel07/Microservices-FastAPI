from fastapi import APIRouter, UploadFile, File

from domain.file_processor import FileProcessor

router = APIRouter()


@router.post("/file/enviar_dados", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def enviar_dados(file: UploadFile = File(...)):
    return await FileProcessor().upload_file(file)

@router.get("/file/listar_arquivos",
            summary="Listar Arquivos Enviados",
            description="Este endpoint retorna uma lista dos arquivos enviados.")
async def listar_arquivos():
    return await FileProcessor().list_files()