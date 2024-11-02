from fastapi import (
    APIRouter, UploadFile, File, Query
)
from domain.file_processor import FileProcessor
from services.api_client import get_token


router = APIRouter()


@router.post('/generate/token',
             summary='Retorna um token de acesso',
             description='Rota para testes de geração de token. ' \
                'Use o usuário \'flask\' e senha \'flask123\' para autenticar.')
async def generate_token(
    user=Query(..., alias='USUÁRIO', max_length=100, example="flask"),
    pswd=Query(..., alias='SENHA', max_length=255, example="flask123")
):
    return get_token(user, pswd)

@router.get("/file/list",
            summary="Listagem de dados",
            description="Essa rota recupera informações do banco de dados.")
async def listar_arquivos():
    return await FileProcessor().list_files()

@router.post("/file/upload/base-incidencia", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def upload_base_incidencia(
    file: UploadFile = File(..., description='Arquivo a ser carregado.')
):
    return await FileProcessor().send_tributo(file)

@router.post("/file/upload/tributo-competencia", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def upload_tributo_competencia(
    file: UploadFile = File(..., description='Arquivo a ser carregado.')
):
    return await FileProcessor().upload_file(file)