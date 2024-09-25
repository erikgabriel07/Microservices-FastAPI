import csv
import json
import os
from fastapi import HTTPException, status, UploadFile


class FileProcessor:
    def __init__(self):
        self.directory = 'data'
        # Cria a pasta caso não exista
        os.makedirs(self.directory, exist_ok=True)  

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
                    valor = row.get("Valor da Receita Tributária", "")

                    if "," in valor:
                        row["Valor da Receita Tributária"] = valor[:valor.find(",") + 3]

                    # Remove chaves vazias
                    row = {key: value for key, value in row.items() if key}
                    data_to_save.append(row)

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