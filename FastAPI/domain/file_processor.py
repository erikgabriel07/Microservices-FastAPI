import csv
from fastapi import (
    HTTPException, status, UploadFile,
    Request, Response
)
from services.api_client import send_data, list_file


class FileProcessor:
    def __init__(self, request: Request, response: Response) -> None:
        self.request = request
        self.response = response
        self.token = request.cookies.get('access_token', None)

    def __gen_auth_header(self) -> dict:
        """Gera o cabeçalho de autorização com o token."""
        access_token = None
        try:
            cookies = self.response.headers.get('set-cookie').split(';')[0]
            access_token = cookies.split('=')[1]
        except Exception as e:
            pass
        token = self.token if self.token else access_token
        return {'Authorization': f'Bearer {token}'}

    async def list_files(self, page, per_page, bi: bool = False, tc: bool = False):
        """
        Lista arquivos disponíveis, com parâmetros opcionais para tipos específicos de arquivos.
        :param bi: Filtro opcional para arquivos do tipo 'Base de Incidência'.
        :param tc: Filtro opcional para arquivos do tipo 'Tributo e Competência'.
        :return: Lista de arquivos.
        """
        return await list_file(self.__gen_auth_header(), page, per_page, bi, tc)

    async def send_data(self, file: UploadFile):
        """
        Realiza o upload de um arquivo CSV, converte seu conteúdo para JSON e envia como uma lista para a API FLASK.
        :param file: Arquivo CSV enviado.
        :return: Mensagem de sucesso ou erro.
        """


        # Verifica se o arquivo é um CSV
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Apenas arquivos CSV são aceitos"
            )

        try:
            # Lê o conteúdo do arquivo e decodifica como texto
            conteudo = await file.read()

            # Remove o BOM e divide o conteúdo em linhas
            arquivo_decodificado = conteudo.decode('utf-8-sig').splitlines()

            # Inicializa o CSV reader e cria uma lista para armazenar os dados processados
            csv_reader = csv.DictReader(arquivo_decodificado)
            data_to_send = []

            # Processa cada linha do arquivo
            for row in csv_reader:
                # Limita o campo 'Valor_da_Receita_Tributaria' a duas casas decimais
                valor = row.get("Valor_da_Receita_Tributaria", "")
                if "." in valor:
                    row["Valor_da_Receita_Tributaria"] = valor[:valor.find(".") + 3]

                data_to_send.append(row)

            # Envia a lista processada para a API
            send_data(data_to_send, self.__gen_auth_header(), file)

            return {"message": f"Arquivo {file.filename} processado e enviado com sucesso"}



        except Exception as e:

            error_message = str(e)

            if "401 Client Error" in error_message and "UNAUTHORIZED" in error_message:

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token de autenticação não definido. Por favor, defina o token antes de enviar dados."
                )

            else:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Falha ao processar o arquivo CSV: {error_message}"
                )