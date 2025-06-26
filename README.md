# MeAjuda.ai - Assistente Parental Inteligente

![MeAjuda.ai Logo](app/streamlit/imgs/logo_meajuda_v4.png)

## Sobre o Projeto

**MeAjuda.ai** é um assistente virtual especializado em orientação parental, desenvolvido como Trabalho de Conclusão de Curso (TCC) para o módulo de Inteligência Artificial da **Escola da Nuvem**. 

Este chatbot foi criado para apoiar pais, mães e tutores nos desafios diários da educação dos filhos, oferecendo orientação baseada em conceitos de parentalidade positiva, disciplina consciente e desenvolvimento infantil.

## Objetivos

- Fornecer orientação parental acessível e baseada em evidências
- Oferecer suporte emocional e estratégias práticas para pais e tutores
- Promover a parentalidade positiva e o desenvolvimento saudável das crianças
- Demonstrar a aplicação prática de IA generativa em cenários reais

## Características Principais

### Assistente IA Especializado
- **Personalidade empática**: Tom acolhedor, calma e encorajadora
- **Expertise em parentalidade**: Baseado em conceitos de desenvolvimento infantil
- **Linguagem acessível**: Evita jargões técnicos, foca em clareza

### Funcionalidades do Chat
- Interface conversacional intuitiva
- Histórico de conversas persistente
- Capacidade de editar e regenerar mensagens
- Múltiplas sessões de chat organizadas

### Diretrizes de Segurança
- **Não faz diagnósticos médicos**: Encaminha para profissionais quando necessário
- **Não prescreve medicamentos**: Mantém foco em orientação comportamental
- **Limites éticos claros**: Segue diretrizes rigorosas de responsabilidade

### Sistema de Autenticação
- Login seguro com persistência de sessão
- Proteção por cookies com assinatura HMAC
- Interface de autenticação personalizada

## Arquitetura Técnica

### Frontend
- **Streamlit**: Interface web responsiva e intuitiva
- **CSS customizado**: Design focado na experiência do usuário
- **JavaScript**: Melhorias de interação (Enter para enviar, etc.)

### Backend & IA
- **Amazon Bedrock**: Integração com modelos de IA generativa (Claude)
- **AWS SDK (Boto3)**: Comunicação com serviços AWS
- **Inference Profiles**: Otimização de performance e custos

### Segurança & Autenticação
- **HMAC**: Assinatura segura de cookies
- **Gestão de sessões**: Controle de acesso baseado em tempo
- **Validação de entrada**: Proteção contra inputs maliciosos

## Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Conta AWS com acesso ao Bedrock
- Credenciais AWS configuradas

### 1. Clone o Repositório
```bash
git clone https://github.com/Grupo-2-BRSAO179/MeAjuda.ai.git
cd MeAjuda.ai
```

### 2. Instale as Dependências
```bash
cd app
pip install -r requirements.txt
```

### 3. Configure as Credenciais AWS
Crie o arquivo `.env` na pasta `app/streamlit/`:
```properties
AWS_PROFILE=seu-perfil-aws
ACCESS_KEY=sua-access-key
SECRET_TOKEN=seu-secret-token
```

### 4. Execute a Aplicação
```bash
cd streamlit
streamlit run app.py
```

## 🔧 Configuração AWS

### Bedrock Setup
1. Habilite o Amazon Bedrock na sua conta AWS
2. Solicite acesso aos modelos Claude (Anthropic)
3. Configure o Inference Profile ARN no arquivo `app.py`

### Permissões IAM Necessárias
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:*:*:inference-profile/*"
        }
    ]
}
```

## 🎮 Como Usar

### 1. Acesso ao Sistema
- **Usuário**: ``
- **Senha**: ``

### 2. Iniciando uma Conversa
1. Faça login na aplicação
2. Clique em "Nova Conversa" ou use uma existente
3. Digite sua pergunta sobre parentalidade no campo de texto
4. Pressione Enter ou clique em "Enviar"

### 3. Exemplos de Perguntas
- "Meu filho de 3 anos faz birra toda vez que digo não. O que posso fazer?"
- "Como estabelecer limites sem gritar com as crianças?"
- "Estratégias para lidar com a ansiedade de separação?"

## Estrutura do Projeto

```
MeAjuda.ai/
├── app/
│   ├── streamlit/
│   │   ├── app.py              # Aplicação principal Streamlit
│   │   ├── functions.py        # Funções auxiliares e integração AWS
│   │   ├── auth_middleware.py  # Sistema de autenticação
│   │   ├── imgs/              # Imagens e logos
│   │   └── .env               # Variáveis de ambiente
│   └── requirements.txt        # Dependências Python
└── README.md                   # Este arquivo
```

## Segurança e Privacidade

- **Dados não armazenados**: Conversas são mantidas apenas durante a sessão
- **Autenticação segura**: Sistema de cookies com assinatura HMAC
- **Limites éticos**: IA programada para não fazer diagnósticos médicos
- **Encaminhamento profissional**: Direciona para especialistas quando necessário

## Contexto Acadêmico

Este projeto foi desenvolvido como parte do programa da **Escola da Nuvem**, demonstrando:

- **Aplicação prática de IA**: Uso de modelos de linguagem em cenário real
- **Integração cloud**: Utilização de serviços AWS para IA generativa
- **Desenvolvimento full-stack**: Frontend e backend integrados
- **Responsabilidade ética**: Implementação de diretrizes de segurança em IA

## Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework web
- **Amazon Bedrock** - Modelos de IA
- **Boto3** - SDK AWS
- **PyPDF2** - Processamento de PDFs
- **Pandas** - Manipulação de dados
- **HMAC/Hashlib** - Segurança e autenticação

## Contribuição

Este é um projeto acadêmico, mas sugestões e melhorias são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto foi desenvolvido para fins educacionais como parte do programa da Escola da Nuvem.

## Autor

Desenvolvido por **Angela, Leonardo, Lila, Rodrigo, Sarah** como Trabalho de Conclusão de Curso para o módulo de IA da Escola da Nuvem.

## Suporte

Para dúvidas sobre o projeto:
- Abra uma [Issue](https://github.com/Grupo-2-BRSAO179/MeAjuda.ai/issues)

---

**Importante**: Este assistente virtual é uma ferramenta de apoio e orientação. Em situações que requerem avaliação profissional, sempre procure ajuda de pediatras, psicólogos infantis ou outros especialistas qualificados.

**Escola da Nuvem** - Capacitando profissionais para o futuro da computação em nuvem
