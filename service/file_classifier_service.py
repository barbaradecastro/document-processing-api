def classify_payment(dados: dict) -> str:
    forma = dados.get("forma_pgto", "").lower()
    if "dinheiro" in forma or "pix" in forma or "cash" in forma:
        return "dinheiro"
    return "outros" 











