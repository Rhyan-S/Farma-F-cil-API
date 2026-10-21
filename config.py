class Config:
    # ----------------------------------------------------
    # CONFIGURAÇÃO DO BANCO DE DADOS (MariaDB via PyMySQL)
    # Servidor: 127.0.0.1 (local) | Usuário: root | Senha: Vazia
    # Banco de Dados: medicamentosdb (Conforme seu dump SQL)
    # ----------------------------------------------------
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/medicamentosdb'
    
    # Desabilita o rastreamento de modificações
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mantém a ordem das chaves JSON como definida (para respostas previsíveis)
    JSON_SORT_KEYS = False
    
    # Configuração de CORS padrão (permite acesso de qualquer origem em ambiente local)
    CORS_HEADERS = 'Content-Type'
