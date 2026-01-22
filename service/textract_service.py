import boto3
import os
import re
from typing import Dict, Any

def extract_text_from_textract(image_bytes: bytes, region: str = None) -> Dict[str, Any]:
    """Extrai texto de uma imagem usando AWS Textract ou mock."""
    
    try:
        # Usando analyze_document para capturar campos de formulários
        textract = boto3.client(
            'textract',         
            region_name=os.getenv("REGION")
        )
        
        # Faz a chamada ao Textract para detectar o texto no documento
        response = textract.analyze_document(
            Document={'Bytes': image_bytes},
            FeatureTypes=["FORMS"]  # Usando "FORMS" para extração de campos estruturados
        )

        # Extrai campos específicos com base na estrutura do documento
        campos_extraidos = _extrair_campos_form(response.get("Blocks", []))

        # Garantir que os campos sejam texto antes de retorná-los
        texto_extraido = " ".join([value for key, value in campos_extraidos.items() if isinstance(value, str)])

        return texto_extraido

    except Exception as e:
        raise RuntimeError(f"Erro ao processar com Textract: {str(e)}")


def _extrair_campos_form(blocks):
    campos = {}
    block_map = {block["Id"]: block for block in blocks}
    
    # Itera sobre os blocks para encontrar KEY_VALUE_SET
    for block in blocks:
        if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
            key = _get_text(block, block_map)
            if key and key.strip():  # Garantir que a chave não seja vazia
                value_block = next(
                    (rel for rel in block.get("Relationships", []) if rel["Type"] == "VALUE"),
                    None
                )
                if value_block:
                    for value_id in value_block["Ids"]:
                        value = _get_text(block_map[value_id], block_map)
                        if value:  # Garantir que o valor não seja vazio
                            campos[key] = value  # Não usamos mais .lower()
    return campos


def _get_text(block, block_map):
    texto = []
    for rel in block.get("Relationships", []):
        if rel["Type"] == "CHILD":
            for cid in rel["Ids"]:
                word = block_map[cid]
                if word["BlockType"] in ["WORD", "SELECTION_ELEMENT"]:
                    texto.append(word.get("Text", ""))
    return " ".join(texto)

