import csv
import json
import os
from fastapi import HTTPException, status, UploadFile


class FileProcessor:
    def __init__(self):
        self.directory = 'data'

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
                csv_reader = csv.DictReader(arquivo_decodificado, delimiter=';')
                data_to_save = []

                for row in csv_reader:

                    # Remove chaves vazias e converte valores numéricos
                    cleaned_row = {key: value.replace(',', '.') if key in ["Valor da Receita Tributária", "Percentual do PIB"] else value 
                                   
                                   # Remove chaves vazias
                                   for key, value in row.items() if key.strip()}  
                    data_to_save.append(cleaned_row)

                # Salva os dados em formato JSON na pasta 'data'
                json_filename = os.path.join(self.directory, f"{file.filename.rsplit('.', 1)[0]}.json")
                with open(json_filename, 'w', encoding='utf-8') as json_file:

                    # Define ensure_ascii como False
                    json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)  

                return {"mensagem": f"Arquivo {file.filename} processado e salvo como JSON com sucesso"}
            
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