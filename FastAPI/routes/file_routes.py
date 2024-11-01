from fastapi import (
    APIRouter, UploadFile, File
)
from domain.file_processor import FileProcessor


router = APIRouter()


@router.get("/file/list",
            summary="Listagem de dados",
            description="Essa rota recupera informações do banco de dados")
async def listar_arquivos():
    return await FileProcessor().list_files()

@router.post("/file/upload/base-incidencia", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def upload_base_incidencia(
    file: UploadFile = File(..., description='Arquivo a ser carregado.')
):
    return await FileProcessor().upload_file(file)

@router.post("/file/upload/tributo-competencia", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def upload_tributo_competencia(
    file: UploadFile = File(..., description='Arquivo a ser carregado.')
):
    return await FileProcessor().upload_file(file)