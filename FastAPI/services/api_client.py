import requests
from fastapi import (
    Response, Request, status as s,
)
from config.urls import Flask_URL as url
from fastapi.exceptions import HTTPException


async def get_token(user, pwd, Response: Response, Request: Request):
    cookies = Request.cookies
    try:
        if cookies:
            header = dict(Authorization=f'Bearer {cookies.get("access_token")}')
            response = requests.post(url.FLASK_LOGIN_ROUTE, headers=header,
                                    json={'user': user, 'pwd': pwd})
        else:
            response = requests.post(url.FLASK_LOGIN_ROUTE, json={'user': user, 'pwd': pwd})
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=s.HTTP_400_BAD_REQUEST, detail={'mensagem': str(e)})
    
    if response.status_code == 200:
        data = response.json()
        Response.set_cookie('access_token', data.get('access_token'),
                            max_age=600, httponly=True, samesite='lax')
        Response.set_cookie('refresh_token', data.get('refresh_token'),
                            max_age=86400, httponly=True, samesite='lax')
    return response.json()


async def verify_token_expiration(Request: Request):
    cookies = Request.cookies
    try:
        if not cookies.get('access_token') and cookies.get('refresh_token'):
            header = dict(Authorization=f'Bearer {cookies.get("refresh_token")}')
            response = requests.post(url.FLASK_REFRESH_TOKEN_ROUTE, headers=header)
            response.raise_for_status()
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=s.HTTP_400_BAD_REQUEST, detail={'mensagem': str(e)})

    return response.json()


async def verify_task_status(Response: Response, Request: Request, task_id: str):
    verification = await verify_token_expiration(Request)
    if verification:
        Response.set_cookie('access_token', verification.get('access_token'),
                            max_age=600, httponly=True, samesite='lax')
        cookies = Response.headers.get('set-cookie').split(';')[0]
        access_token = cookies.split('=')[1]
    else:
        cookies = Request.cookies
        access_token = cookies.get('access_token')
    
    header = lambda token: dict(Authorization=f'Bearer {token}')
    try:
        full_url = url.FLASK_TASK_STATUS_URL + task_id
        response = requests.get(full_url, headers=header(access_token))
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=s.HTTP_400_BAD_REQUEST, detail={'mensagem': str(e)})
    
    return response.json()


async def list_file(header, page, per_page, bi=False, tc=False):
    try:
        if bi == tc:
            raise HTTPException(
                status_code=s.HTTP_400_BAD_REQUEST,
                detail={'mensagem': 'Apenas um e somente um parâmetro pode ser selecionado.'}
            )

        parameters = f'?page={page}&per_page={per_page}'
        response = requests.get(
            url.FLASK_LIST_DATA_URL + parameters,
            headers=header,
            json={'bi': bi, 'tc': tc}
        )
        response.raise_for_status()

    except Exception as e:
        raise HTTPException(
            status_code=s.HTTP_400_BAD_REQUEST,
            detail={'mensagem': 'Erro durante o processamento da requisição.', 'error': str(e)}
        )
    return response.json()


def send_data(data, header, file):
    try:
        # Define a URL com base no tipo de arquivo
        if file.filename == "Tabela 1 - Base de Incidência.csv":
            url_to_use = url.FLASK_BASE_INCIDENCIA_URL
        elif file.filename == "Tabela 2 - Tributo e Competência.csv":
            url_to_use = url.FLASK_TRIBUTO_COMPETENCIA_URL
        else:
            raise ValueError(
                "O Arquivo enviado é inválido ou incompatível com o serviço solicitado."
            )

        # Faz a requisição usando a URL apropriada
        response = requests.post(url_to_use, json=data, headers=header)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao enviar dados: {e}")

    except ValueError as ve:
        raise Exception(ve)
