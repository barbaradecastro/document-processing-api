import logging
import base64
import json
import re
import os
from service.unzip_service import extract_files_from_zip
from service.send_to_s3_service import save_to_s3
from service.textract_service import extract_text_from_textract  # Importando a função do Textract
from service.nlp_service import refine_with_nlp
from service.refinement_with_llm_service import refine_with_llm
from service.file_classifier_service import classify_payment

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": "Erro: campo 'body' ausente. Verifique se está enviando como application/zip"
            }

        # 1. Recebe o zip via API Gateway (base64)
        zip_file_bytes = base64.b64decode(event["body"])

        # 2. Extrai os arquivos
        imagens = extract_files_from_zip(zip_file_bytes)
        logger.info(f"Arquivos encontrados: {[img['filename'] for img in imagens]}")

        resultados = []

        # 3 a 7. Processa cada imagem
        for imagem in imagens:
            try:
                initial_destination_folder = "notas"
                s3_url = save_to_s3(imagem, initial_destination_folder)

                textract_resultado = extract_text_from_textract(imagem["content"])
                logger.info(f"Texto extraído: {textract_resultado}")

                # Garantir que o textract_resultado seja uma string, ou pegar uma chave específica
                if isinstance(textract_resultado, dict):
                    textract_resultado = " ".join([textract_resultado[key] for key in textract_resultado if isinstance(textract_resultado[key], str)])

                refined_data = refine_with_nlp(textract_resultado)
                refined_data_with_llm = refine_with_llm(refined_data, textract_resultado)
                payment_method = classify_payment(refined_data_with_llm)

                if payment_method == "dinheiro":
                    final_destination_folder = os.getenv("PASTA_1")
                else:
                    final_destination_folder = os.getenv("PASTA_2")
                    s3_url_final = save_to_s3(imagem, final_destination_folder)

                
                resultados.append(refined_data_with_llm)

            except Exception as e:
                logger.error(f"Erro no processamento da imagem {imagem['filename']}: {str(e)}")
                continue

        # 8. Retorna JSON
        return {
            "statusCode": 200,
            "body": json.dumps(resultados, ensure_ascii=False)
        }

    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"Erro: {str(e)}"
        }
