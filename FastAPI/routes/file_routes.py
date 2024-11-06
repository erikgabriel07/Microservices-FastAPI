from fastapi import (
    APIRouter, UploadFile, File, Query, Response, Request
)
from fastapi.exceptions import HTTPException
from domain.file_processor import FileProcessor
from services.api_client import get_token, verify_token_expiration, verify_task_status


router = APIRouter()


@router.get('/status_da_requisicao/{task_id}',
            summary='Verificar status da requisição',
            description='Verifica o status de uma requisição.')
async def get_task_status(
    response: Response,
    request: Request,
    task_id: str
):
    return await verify_task_status(response, request, task_id)

@router.post('/generate/token',
             summary='Retorna um token de acesso',
             description='Rota para testes de geração de token. ' \
                'Use o usuário \'flask\' e senha \'flask123\' para autenticar.')
async def generate_token(
    response: Response,
    request: Request,
    user=Query(..., alias='USUÁRIO', max_length=100, example='flask'),
    pswd=Query(..., alias='SENHA', max_length=255, example='flask123')
):
    return await get_token(user, pswd, response, request)

@router.get('/file/list',
            summary='Listagem de dados',
            description='Essa rota recupera informações do banco de dados.')
async def listar_arquivos(
    response: Response,
    request: Request,
    bi: bool=Query(False, alias='BaseIncidencia'),
    tc: bool=Query(False, alias='TributoCompetencia'),
    page: int=Query(1, ge=1, description='Número da página.'),
    per_page: int=Query(100, ge=100, description='Total de itens que cada página deve ter.')
):
    try:
        verification = await verify_token_expiration(request)
        if verification:
            response.set_cookie('access_token', verification.get('access_token'),
                                max_age=600, httponly=True, samesite='lax')
        
        return await FileProcessor(request, response).list_files(page, per_page, bi, tc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/file/upload/upload_csv',
             summary = 'Enviar Dados do Arquivo CSV', 
             description='Este endpoint recebe um arquivo de Base de Incidência ' \
                 'ou Tributo e Competência CSV e retorna uma mensagem de confirmação.')
async def upload_csv(
    response: Response,
    request: Request,
    file: UploadFile = File(..., description='Arquivo Base de Incidência ou Tributo e Competência CSV.')
):
    try:
        verification = await verify_token_expiration(request)
        if verification:
            response.set_cookie('access_token', verification.get('access_token'),
                                max_age=600, httponly=True, samesite='lax')
        
        return await FileProcessor(request, response).send_data(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

