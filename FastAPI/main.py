from fastapi import FastAPI, Request, status as s
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import init_routes
from uvicorn import run as startapp


def main():
    app = FastAPI(
        title='Processamento de Arquivos',
        description='API voltada para processamento de gerenciamento de dados ' \
        'públicos. Essa API recebe arquivos CSV de dados abertos e processa-os' \
        ' enviando para uma API desenvolvida em Flask que faz o trabalho de ar' \
        'mazenar e processar essas informações em um banco de dados.',
        debug=True) # debug somente em desenvolvimento
    init_routes(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True,
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=s.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'message': 'Ocorreu um erro durante a requisição!',
                     'details': exc.errors()}
        )
    
    startapp(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
