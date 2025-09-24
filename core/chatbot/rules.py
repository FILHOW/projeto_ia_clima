import pandas as pd

def answer_clima_questions(question: str, metrics: dict, coef_df: pd.DataFrame):
    """
    Responde perguntas sobre o modelo de clima, métricas, variáveis importantes, pipeline e privacidade.
    - question: pergunta do usuário
    - metrics: dicionário de métricas do modelo
    - coef_df: DataFrame com variáveis e coeficientes do modelo
    """
    q = (question or "").lower()

    if "importan" in q or "importân" in q or "variáve" in q or "features" in q:
        if coef_df is not None and not coef_df.empty:
            top = coef_df.sort_values(by="Coeficiente", key=abs, ascending=False).head(5)
            top_str = ", ".join(top["Variável"].astype(str))
            return f"As variáveis mais influentes são: {top_str}. (Baseado nos coeficientes do modelo)"
        else:
            return "Os coeficientes do modelo ainda não estão disponíveis. Treine ou carregue o modelo."

    if "métric" in q or "score" in q or "acur" in q or "rmse" in q or "mae" in q or "r2" in q:
        if metrics:
            return f"Métricas do modelo: {metrics}"
        else:
            return "As métricas do modelo ainda não estão disponíveis. Treine ou carregue o modelo."

    if "como foi treinado" in q or "pipeline" in q or "como funciona" in q:
        return ("O pipeline do projeto aplica ETL nos dados brutos, faz one-hot encoding para variáveis categóricas, "
                "e treina um modelo de Regressão Linear para prever precipitação. O modelo é salvo e pode ser reutilizado.")

    if "privacid" in q or "lgpd" in q:
        return ("No MVP, evitamos dados sensíveis e não persistimos dados pessoais. "
                "Para produção: aplicar anonimização, consentimento expresso, minimização e auditoria de dados.")

    return ("Posso responder sobre variáveis importantes, métricas do modelo, pipeline e privacidade. "
            "Pergunte, por exemplo: 'Quais variáveis mais importam?' ou 'Quais as métricas do modelo?'")