from fastapi import APIRouter, Path, UploadFile, File

from domain.file_processor import FileProcessor

router = APIRouter()


@router.post("/file/enviar_dados", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def enviar_dados(file: UploadFile = File(...)):
    return await FileProcessor().upload_file(file)


