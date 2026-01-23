# 📄 Extração e Classificação de Notas Fiscais com AWS

## 📌 Objetivo

Construir uma solução automatizada para receber imagens de notas fiscais em arquivos ZIP, extrair informações relevantes utilizando AWS Textract, refinar os dados com NLP e LLM, classificar a forma de pagamento e armazenar os resultados de forma organizada em buckets S3.

## ✨ Funcionalidades

- Recebimento de arquivos .zip contendo imagens de notas fiscais via API Gateway
- Extração de texto utilizando AWS Textract
- Processamento de texto com NLP (NLTK)
- Refinamento semântico com LLM via Amazon Bedrock (Nova Pro)
- Classificação da forma de pagamento (dinheiro ou outros)
- Armazenamento em pastas separadas no Amazon S3 com base na classificação
- Retorno estruturado em formato JSON com os dados extraídos da nota fiscal

## 👟 Passos Seguidos

- Configuração da API REST  
  https://rxz4qmfjh0.execute-api.us-east-1.amazonaws.com/invoice/api/v1/invoice

- Construção da função Lambda principal (lambda_function.py) como ponto de entrada

- Implementação do serviço de extração de imagens a partir de arquivos .zip  
  (unzip_service.py)

- Integração com Amazon S3 para upload das imagens  
  (send_to_s3_service.py)

- Extração de texto com AWS Textract  
  (textract_service.py)

- Refino textual com técnicas de NLP  
  (nlp_service.py)

- Refinamento semântico com LLM via Amazon Bedrock  
  (refinement_with_llm_service.py)

- Classificação da nota com base na forma de pagamento  
  (file_classifier_service.py)

- Estruturação e retorno final da resposta pela API

## 👩‍💻 Tecnologias Utilizadas

- Python
- AWS Lambda
- Amazon API Gateway
- Amazon S3
- Amazon Textract
- Amazon Bedrock (Nova Pro)
- NLTK (Natural Language Toolkit)
- Boto3
- Regex

## 🚧 Dificuldades Conhecidas

### Regex
Ajustar expressões para extrair informações específicas (CNPJ, valor, data) foi trabalhoso devido à grande variação entre layouts de notas fiscais.

### Prompt Engineering
Definir um prompt que guiasse o LLM a responder de forma objetiva e padronizada exigiu múltiplos testes.

### Configuração das Layers
A inclusão de dependências externas (NLTK, Boto3 com Bedrock) nas layers do Lambda exigiu empacotamento manual e controle de compatibilidade.

### API Gateway
Configurar corretamente o recebimento do corpo da requisição como base64 e o mapeamento para a Lambda exigiu ajustes finos.

## 📂 Estrutura do Código Fonte

.
├── lambda_function.py
└── service/
    ├── file_classifier_service.py
    ├── nlp_service.py
    ├── refinement_with_llm_service.py
    ├── send_to_s3_service.py
    ├── textract_service.py
    └── unzip_service.py

## 🚀 Como Utilizar o Projeto

### 1. Implantação na AWS Lambda

Faça o deploy do código compactado (.zip) com todas as dependências incluídas  
ou utilize um container AWS Lambda.

### 2. Configuração das Variáveis de Ambiente

- REGION: Região AWS (ex: us-east-1)
- PASTA_1: Nome da pasta no S3 para notas pagas em dinheiro
- PASTA_2: Nome da pasta no S3 para demais notas
- USE_BEDROCK: True ou False para ativar/desativar o uso do LLM

### 3. Chamada via API Gateway

Envie um arquivo .zip com imagens de notas fiscais em base64 no body da requisição POST.

Exemplo de retorno JSON:

{
  "nome_emissor": "<nome-fornecedor>",
  "CNPJ_emissor": "00.000.000/0000-00",
  "endereco_emissor": "<endereco-fornecedor>",
  "CNPJ_CPF_consumidor": "000.000.000-00",
  "data_emissao": "00/00/0000",
  "numero_nota_fiscal": "123456",
  "serie_nota_fiscal": "123",
  "valor_total": "0000.00",
  "forma_pgto": "<dinheiro|pix|outros>"
}

## ✨ Autora

👩‍💻 Bárbara Castro

## 📜 Licença

Este projeto é de autoria de Bárbara Castro.  
O código é disponibilizado exclusivamente para fins de visualização como portfólio.

❌ Não é permitida a cópia, modificação ou distribuição sem autorização prévia.
