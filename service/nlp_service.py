import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.data.path.append("/opt/python/lib/python3.10/nltk_data")

def refine_with_nlp(texto: str) -> dict:
    if not isinstance(texto, str):  # Verifica se o texto é uma string
        raise ValueError("Texto deve ser uma string.")
    
    texto_original = texto

    # Mantém acentos e cedilha, remove só o necessário
    texto_limpo = re.sub(r"[^a-zA-Z0-9çãẽíóúáéóàêôõâîúü\s:.,/-]", "", texto_original)

    # Tokenização
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(texto_limpo)

    # Remover stopwords
    tokens_filtrados = [w for w in tokens if w not in stopwords.words("portuguese")]
    texto_final = " ".join(tokens_filtrados)

    # Expressões regulares 

    nome_emissor_match = re.search(r'(nome\s*fornecedor|nome)\s*[:\-]?\s*([A-Za-zÁáÉéÍíÓóÚú\s]+)', texto_limpo)
    cnpj_emissor_match = re.search(r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}', texto_limpo)
    cpf_consumidor_match = re.search(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', texto_limpo)
    data_emissao_match = re.search(r'\d{2}[\/\-]?\d{2}[\/\-]?\d{4}', texto_limpo)

    numero_nf_match = re.search(r'(n[^\w]{0,2}f|nf)[^\d]*(\d+)', texto_limpo, re.IGNORECASE)
    serie_match = re.search(r'serie[s,"série", "serie", "0003]?:?\s*(\d+)', texto_limpo, re.IGNORECASE)

    valor_total_match = re.search(r'(valor[\s:]*total)[^\d]*(\d+[,.]?\d*)', texto_limpo, re.IGNORECASE)
    forma_pgto_match = re.search(r'(forma[\s:]*de[\s:]*pagamento)[^\w]*(dinheiro|cart[aã]o|pix)', texto_limpo, re.IGNORECASE)

    # Adicionando a expressão regular para capturar o endereço (independente de "rua", "logradouro" ou "endereço")
    endereco_emissor_match = re.search(r'(rua|logradouro|endereço|av\.?|av|sn|SN|Casemiro,\s?1|Romeu\s?2|n°?1|travessa|alameda|avenida|praça)[\s:]*([A-Za-z0-9\s,]*)(\d+)', texto_limpo, re.IGNORECASE)

    # Extração dos grupos
    nome_emissor = nome_emissor_match.group(2) if nome_emissor_match else None
    cnpj_emissor = cnpj_emissor_match.group() if cnpj_emissor_match else None
    endereco_emissor = endereco_emissor_match.group() if endereco_emissor_match else None

    cpf_consumidor = cpf_consumidor_match.group() if cpf_consumidor_match else None
    data_emissao = data_emissao_match.group() if data_emissao_match else None

    numero_nf = numero_nf_match.group(2) if numero_nf_match else None
    serie = serie_match.group(1) if serie_match else None

    valor_total = valor_total_match.group(2) if valor_total_match else None
    forma_pgto = forma_pgto_match.group(2) if forma_pgto_match else None

    # Extração do endereço
    endereco_emissor = endereco_emissor_match.group(2) if endereco_emissor_match else None

    # Retorno com os dados extraídos
    return {
        "nome_emissor": nome_emissor,
        "CNPJ_emissor": cnpj_emissor,
        "endereco_emissor": endereco_emissor,
        "CNPJ_CPF_consumidor": cpf_consumidor,        
        "data_emissao": data_emissao,
        "numero_nota_fiscal": numero_nf,
        "serie_nota_fiscal": serie,
        "valor_total": valor_total,
        "forma_pgto": forma_pgto,
    }


