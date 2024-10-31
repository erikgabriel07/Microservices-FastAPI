from fastapi import (
    APIRouter, UploadFile, File, Query,
)

from domain.file_processor import FileProcessor
from domain.route_parameters import verify_id_parameter


router = APIRouter()


@router.get("/file/list",
            summary="Listagem de dados",
            description="Essa rota recupera informações do banco de dados")
async def listar_arquivos():
    return await FileProcessor().list_files()

@router.post("/file/upload/base-incidencia", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def upload_base_incidencia(file: UploadFile = File(...)):
    return await FileProcessor().upload_file(file)

@router.post("/file/upload/tributo-competencia", 
             summary = "Enviar Dados do Arquivo CSV", 
             description="Este endpoint recebe um arquivo CSV e retorna uma mensagem de confirmação.")
async def upload_tributo_competencia(file: UploadFile = File(...)):
    return await FileProcessor().upload_file(file)

@router.patch("/file/delete/",
            summary="Remoção de dados",
            description="Essa rota remove dados do banco de dados")
@verify_id_parameter
async def delete(
    id: int = Query(None, alias='Identifier', ge=0,
                    description='ID do item a ser removido'),
):
    return {'message': 'Data deleted successfully!'}

@router.patch("/file/duplicate/",
            summary="Define se um dado é duplicado",
            description="Essa rota marca um dado no banco de dados como duplicado")
@verify_id_parameter
async def duplicate(
    id: int = Query(None, alias='Identifier', ge=0,
                    description='ID do item a ser marcado como duplicado'),
    value: bool = Query(False, alias='Value',
                        description='Valor a ser configurado')
):
    return {'message': 'Data \'duplicate\' was updated successfully!'}