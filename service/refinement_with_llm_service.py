import os
import json
import boto3

use_bedrock = os.getenv("USE_BEDROCK", "False") == "True"

if use_bedrock:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1"
    )

def refine_with_llm(dados: dict, texto_completo: str) -> dict:
    if not use_bedrock:
        return dados  # Simulação local

    prompt = f"""
Você é um sistema de refinamento de dados de nota fiscal. Abaixo está o JSON extraído automaticamente do Textract:

{json.dumps(dados, ensure_ascii=False, indent=2)}

Baseado nesses dados, retorne os campos preenchidos corretamente no formato abaixo.
Se algum campo estiver ausente ou estiver com valor vazio/null, insira o valor "None".

Formato final esperado:
{{
    "nome_emissor": "",
    "CNPJ_emissor": "",
    "endereco_emissor": "",
    "CNPJ_CPF_consumidor": "",
    "data_emissao": "",
    "numero_nota_fiscal": "",
    "serie_nota_fiscal": "",
    "valor_total": "",
    "forma_pgto": ""
}}

Texto extraído completo da nota fiscal:

{texto_completo}

Por favor, garanta que:
- Datas estejam no formato DD/MM/AAAA
- Valores monetários estejam no formato R$ 1.234,56
- O JSON de saída esteja bem formatado e não contenha texto explicativo.
"""

    print("\n[DEBUG] Prompt enviado ao Bedrock:")
    print(prompt)

    try:
        response = bedrock_client.invoke_model(
            modelId="amazon.nova-pro-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"text": prompt}
                        ]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 2000,
                    "temperature": 0.2,
                    "topP": 0.9
                }
            })
        )

        response1 = json.loads(response["body"].read())

        print("\n[DEBUG] Resposta do Bedrock:")
        print(json.dumps(response1, indent=2, ensure_ascii=False))

        # Correto para Nova Pro:
        message = (
            response1.get("output", {})
            .get("message", {})
            .get("content", [{}])[0]
            .get("text", "")
            .strip()
        )

        if not message:
            raise ValueError("Resposta vazia ou não encontrada na resposta do Bedrock.")

        return _extract_json_from_response(message)

    except Exception as e:
        print(f"[ERROR] Falha na chamada ao Bedrock: {e}")
        return {"erro": f"Erro na LLM: {str(e)}"}


def _extract_json_from_response(text: str) -> dict:
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("JSON não encontrado na resposta da LLM.")
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception as e:
        print(f"[ERROR] Falha ao extrair JSON da resposta: {e}")
        return {"erro": "Não foi possível processar a resposta da LLM"}

