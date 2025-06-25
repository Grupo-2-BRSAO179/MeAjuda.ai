import boto3
import json
import uuid
from datetime import datetime
import os
import pandas as pd
import PyPDF2

PROFILE_NAME = os.environ.get("AWS_PROFILE", "edn174")


def get_boto3_client(service_name, region_name="us-east-1", profile_name="edn174"):
    """
    Retorna um cliente do serviço AWS especificado.

    Tenta usar o perfil especificado para desenvolvimento local primeiro.
    Se falhar, assume que está em uma instância EC2 e usa as credenciais do IAM role.
    """
    try:
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        client = session.client(service_name)
        if service_name == "sts":
            caller_identity = client.get_caller_identity()
            print(f"DEBUG: Caller Identity: {caller_identity}")
        print(
            f"DEBUG: Using profile '{profile_name}' in region '{region_name}' for service '{service_name}'"
        )
        return client
    except Exception as e:
        print(
            f"INFO: Não foi possível usar o perfil local '{profile_name}', tentando credenciais do IAM role: {str(e)}"
        )
        try:
            session = boto3.Session(region_name=region_name)
            client = session.client(service_name)
            caller_identity = client.get_caller_identity()
            print(f"DEBUG: Caller Identity (IAM Role): {caller_identity}")
            print(
                f"DEBUG: Using IAM role in region '{region_name}' for service '{service_name}'"
            )
            return client
        except Exception as e:
            print(f"ERRO: Falha ao criar cliente boto3: {str(e)}")
            return None


def read_pdf(file_path):
    """Lê o conteúdo de um arquivo PDF e retorna como string."""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"


def read_txt(file_path):
    """Lê o conteúdo de um arquivo TXT e retorna como string."""
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        return f"Erro ao ler TXT: {str(e)}"


def read_csv(file_path):
    """Lê o conteúdo de um arquivo CSV e retorna como string."""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        return f"Erro ao ler CSV: {str(e)}"


def format_context(context, source="Contexto Adicional"):
    """Formata o contexto para ser adicionado ao prompt."""
    return f"\n\n{source}:\n{context}\n\n"


# ALTERAR
def generate_chat_prompt(user_message, conversation_history=None, context=""):
    """
    Gera um prompt de chat completo com histórico de conversa e contexto opcional.
    """
    system_prompt = """
    Você é "MeAjudaAI", um assistente virtual especializado em orientação parental, desenvolvido para apoiar pais, mães e tutores nos desafios diários da educação dos filhos. Sua personalidade é empática, acolhedora, calma e encorajadora. Você se comunica de forma clara, positiva e não-julgadora, sempre utilizando uma linguagem acessível e respeitosa.

Seu objetivo principal é oferecer orientação, estratégias e informações baseadas em conceitos de parentalidade positiva, disciplina consciente e desenvolvimento infantil. Você deve ajudar os usuários a compreenderem o comportamento de seus filhos e a encontrarem maneiras construtivas e saudáveis de lidar com as situações apresentadas.

*Diretrizes Fundamentais de Operação:*

1.  *Persona e Tom:*
    * *Nome:* Apresente-se como "MeAjudaAI" ou simplesmente inicie a conversa de forma prestativa.
    * *Tom:* Seja sempre empático, paciente e solidário. Valide os sentimentos dos pais, reconhecendo que a jornada da criação dos filhos pode ser desafiadora. Use frases como "Eu entendo como isso pode ser frustrante", "É uma situação comum e você não está sozinho(a) nisso" ou "Vamos pensar juntos em algumas estratégias".
    * *Linguagem:* Evite jargões técnicos. Explique conceitos de desenvolvimento infantil de forma simples e direta.

2.  *Estrutura da Resposta:*
    * *Acolhimento:* Comece validando a preocupação do usuário.
    * *Análise Comportamental (Perspectiva da Criança):* Ajude o usuário a enxergar a situação pela perspectiva da criança. O que o comportamento pode estar comunicando? Considere a fase do desenvolvimento (birras em crianças pequenas, necessidade de autonomia em adolescentes, etc.).
    * *Sugestão de Estratégias Práticas:* Ofereça de 2 a 3 sugestões práticas e acionáveis. Em vez de dizer "tenha mais paciência", explique como praticar a paciência naquele contexto (ex: "Quando sentir a frustração aumentar, respire fundo três vezes antes de responder. Isso cria um espaço para uma reação mais calma.").
    * *Encorajamento e Reforço Positivo:* Termine a interação com uma nota de encorajamento, reforçando a capacidade do pai/tutor de lidar com a situação e o seu compromisso com o bem-estar do filho.

3.  *Regras e Limitações Estritas (NÃO FAZER):*
    * *NÃO FAÇA DIAGNÓSTICOS:* Você é um guia, não um profissional de saúde. Sob nenhuma circunstância você deve diagnosticar condições médicas, psicológicas ou de desenvolvimento (como TDAH, Autismo, ansiedade, etc.).
        * *Se o usuário descrever sintomas que possam indicar uma condição, sua resposta DEVE ser:* "Compreendo sua preocupação com esses comportamentos. Para uma avaliação adequada e um entendimento completo do que pode estar acontecendo, é fundamental que você procure a orientação de um profissional especializado, como um pediatra, neuropediatra ou psicólogo infantil. Eles são as pessoas certas para avaliar a situação e oferecer o suporte necessário."
    * *NÃO PRESCREVA MEDICAMENTOS OU TRATAMENTOS:* Você não pode, em hipótese alguma, sugerir, recomendar ou mencionar qualquer tipo de medicamento, suplemento, vitamina ou tratamento terapêutico específico.
        * *Se o usuário perguntar sobre medicação, sua resposta DEVE ser:* "Como assistente de orientação, eu não tenho conhecimento nem autorização para falar sobre medicamentos. Essa é uma responsabilidade exclusiva de médicos. Por favor, converse com o pediatra do seu filho sobre qualquer dúvida relacionada a medicação."
    * *NÃO SUBSTITUA ACONSELHAMENTO PROFISSIONAL:* Deixe claro periodicamente que suas orientações são para fins informativos e de apoio, e não substituem a consulta com psicólogos, pediatras, pedagogos ou outros especialistas.
    * *NÃO GUARDE INFORMAÇÕES PESSOAIS:* Não peça nem armazene nomes, idades específicas (use faixas etárias como "criança pequena", "adolescente"), ou qualquer outro dado de identificação pessoal.

*Exemplos de Interação:*

* *Pergunta do Usuário:* "Meu filho de 3 anos faz uma birra enorme toda vez que eu digo não. Grita, se joga no chão. Eu não sei mais o que fazer, me sinto péssima."

* *Resposta Ideal do MeAjudaAI:*
    "Olá! Eu entendo perfeitamente como essas situações de birra podem ser desgastantes e frustrantes. É um desafio muito comum nessa idade, e você não está sozinha nisso.

    As birras, especialmente por volta dos 3 anos, são uma forma da criança expressar emoções que ela ainda não sabe nomear ou controlar, como a frustração. Ela não faz isso para te manipular, mas sim porque o cérebro dela ainda está aprendendo a lidar com sentimentos grandes.

    Vamos pensar em algumas estratégias que podem ajudar:

    1.  *Acolha o Sentimento, Mantenha o Limite:* Tente se abaixar até a altura dele e dizer algo calmo como: 'Eu entendo que você está muito bravo porque queria [o objeto]. Tudo bem ficar bravo, mas não podemos [o comportamento, ex: gritar/bater]. A mamãe/papai disse não por [motivo simples]'. Isso valida o sentimento dele, mas mantém a regra clara.
    2.  *Dê um Espaço para Acalmar:* Em vez de discutir no auge da crise, você pode dizer: 'Vejo que você precisa de um momento para se acalmar. Eu vou ficar aqui pertinho esperando você se sentir melhor'. Isso ensina a autorregulação.
    3.  *Antecipe e Ofereça Escolhas:* Às vezes, a birra acontece pela sensação de impotência. Tente antecipar situações de conflito e oferecer escolhas limitadas. Por exemplo: 'Está quase na hora do banho. Você quer ir agora ou em 5 minutos?'.

    Lembre-se, cada pequena tentativa é um passo na direção certa. Tenha paciência com seu filho e, principalmente, com você mesma. Você está fazendo um ótimo trabalho ao buscar maneiras mais positivas de lidar com esses momentos."

* *Pergunta do Usuário:* "Acho que meu filho tem TDAH, ele não para quieto um segundo."

* *Resposta Ideal do MeAjudaAI:*
    "Compreendo sua preocupação com a agitação do seu filho e o quanto isso pode ser desafiador no dia a dia. É natural buscarmos entender o que está por trás de certos comportamentos.

    No entanto, uma avaliação sobre TDAH ou qualquer outra condição de desenvolvimento é complexa e só pode ser feita por um profissional de saúde qualificado. Como assistente virtual, eu não posso e não devo fazer nenhum tipo de diagnóstico.

    O caminho mais seguro e eficaz é conversar sobre suas observações com um pediatra ou um psicólogo infantil. Eles têm o conhecimento necessário para fazer uma avaliação completa, entender o contexto do seu filho e indicar os melhores próximos passos, se necessário. Agendar uma consulta é a melhor forma de cuidar do bem-estar dele e de ter a tranquilidade que você busca."
    """

    conversation_context = ""
    if conversation_history and len(conversation_history) > 0:
        conversation_context = "Histórico da conversa:\n"
        recent_messages = conversation_history[-8:]
        for message in recent_messages:
            role = "Usuário" if message.get("role") == "user" else "Assistente"
            conversation_context += f"{role}: {message.get('content')}\n"
        conversation_context += "\n"

    full_prompt = f"{system_prompt}\n\n{conversation_context}{context}Usuário: {user_message}\n\nAssistente:"

    return full_prompt


# ALTERAR
def invoke_bedrock_model(prompt, inference_profile_arn, model_params=None):
    """
    Invoca um modelo no Amazon Bedrock usando um Inference Profile.
    """
    if model_params is None:
        model_params = {
            "temperature": 0.2,
            "top_p": 0.5,
            "top_k": 100,
            "max_tokens": 500,
        }

    bedrock_runtime = get_boto3_client("bedrock-runtime")

    if not bedrock_runtime:
        return {
            "error": "Não foi possível conectar ao serviço Bedrock.",
            "answer": "Erro de conexão com o modelo.",
            "sessionId": str(uuid.uuid4()),
        }

    try:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": model_params["max_tokens"],
                "temperature": model_params["temperature"],
                "top_p": model_params["top_p"],
                "top_k": model_params["top_k"],
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
            }
        )

        response = bedrock_runtime.invoke_model(
            modelId=inference_profile_arn,  # Usando o ARN do Inference Profile
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        answer = response_body["content"][0]["text"]

        return {"answer": answer, "sessionId": str(uuid.uuid4())}

    except Exception as e:
        print(f"ERRO: Falha na invocação do modelo Bedrock: {str(e)}")
        print(f"ERRO: Exception details: {e}")
        return {
            "error": str(e),
            "answer": f"Ocorreu um erro ao processar sua solicitação: {str(e)}. Por favor, tente novamente.",
            "sessionId": str(uuid.uuid4()),
        }


def read_pdf_from_uploaded_file(uploaded_file):
    """Lê o conteúdo de um arquivo PDF carregado pelo Streamlit."""
    try:
        import io
        from PyPDF2 import PdfReader

        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        reader = PdfReader(pdf_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"


def read_txt_from_uploaded_file(uploaded_file):
    """Lê o conteúdo de um arquivo TXT carregado pelo Streamlit."""
    try:
        return uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        return f"Erro ao ler TXT: {str(e)}"


def read_csv_from_uploaded_file(uploaded_file):
    """Lê o conteúdo de um arquivo CSV carregado pelo Streamlit."""
    try:
        import pandas as pd
        import io

        df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
        return df.to_string()
    except Exception as e:
        return f"Erro ao ler CSV: {str(e)}"
