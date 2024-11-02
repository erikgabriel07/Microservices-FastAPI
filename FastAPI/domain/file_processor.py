import csv
from fastapi import HTTPException, status, UploadFile
from services.api_client import send_data, list_file

class FileProcessor:
    token = None

    @staticmethod
    def set_token(token):
        FileProcessor.token = token

    @staticmethod
    def get_token():
        return FileProcessor.token
    
    def __gen_auth_header(self):
        return {'Authorization': f'Bearer {self.token}'}

    async def list_files(self, bi=False, tc=False):
        return list_file(self.__gen_auth_header(), bi, tc)

    async def upload_file(self, file: UploadFile):

        """
        Faz o upload de um arquivo CSV, converte para JSON e salva na pasta 'data'.
        :param file: arquivo enviado
        :return: mensagem de sucesso ou erro
        """

        if file.filename.endswith('.csv'):
            try:
                # Decodifica o arquivo para string
                conteudo = await file.read()

                # Remove o BOM
                arquivo_decodificado = conteudo.decode('utf-8-sig').splitlines()  

                # Cria o CSV reader a partir do conteúdo decodificado, especificando o delimitador
                csv_reader = csv.DictReader(arquivo_decodificado)
                data_to_save = []

                for row in csv_reader:

                    # Deixa o valor com apenas 2 casas decimais após a virgula
                    valor = row.get("Valor_da_Receita_Tributaria", "")

                    if "." in valor:
                        row["Valor_da_Receita_Tributaria"] = valor[:valor.find(".") + 3]

                    data_to_save.append(row)  

                return {"message": f"Arquivo {file.filename} processado e salvo como JSON com sucesso"}
            
            except Exception as e:
                
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Falha ao processar o arquivo CSV: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Apenas arquivos CSV são aceitos"
            )

    async def send_tributo(self, file: UploadFile):
        """
        Faz o upload de um arquivo CSV, converte para JSON e envia todas as linhas como uma lista para a API Flask.
        :param file: arquivo enviado
        :return: mensagem de sucesso ou erro
        """
        if file.filename.endswith('.csv'):
            try:
                # Decodifica o arquivo para string
                conteudo = await file.read()

                # Remove o BOM e divide em linhas
                arquivo_decodificado = conteudo.decode('utf-8-sig').splitlines()

                # Cria o CSV reader a partir do conteúdo decodificado
                csv_reader = csv.DictReader(arquivo_decodificado)
                data_to_send = []

                # Processa cada linha e adiciona à lista
                for row in csv_reader:
                    # Limita o valor a 2 casas decimais após a vírgula
                    valor = row.get("Valor_da_Receita_Tributaria", "")
                    if "." in valor:
                        row["Valor_da_Receita_Tributaria"] = valor[:valor.find(".") + 3]

                    data_to_send.append(row)

                # Envia a lista completa para a API Flask
                send_data(data_to_send, self.__gen_auth_header()) # Utilize await se send_insidencia for uma função assíncrona


                return {"message": f"Arquivo {file.filename} processado e enviado com sucesso"}

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Falha ao processar o arquivo CSV: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Apenas arquivos CSV são aceitos"
            )
