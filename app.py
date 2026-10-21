from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db, populate_sample_data
from routes import api_bp
from sqlalchemy import text
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ----------------------------------------------------
    # INICIALIZAÇÃO DAS EXTENSÕES
    # ----------------------------------------------------
    db.init_app(app) # Vincula a instância do SQLAlchemy ao app Flask
    CORS(app)       # Habilita o CORS

    # ----------------------------------------------------
    # REGISTRO DOS BLUEPRINTS (MÓDULOS DE ROTAS)
    # ----------------------------------------------------
    app.register_blueprint(api_bp)

    # =================== ERROR HANDLERS (Manipuladores de Erro) ===================
    
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso não encontrado'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Requisição inválida'}), 400

    @app.errorhandler(500)
    def internal_error(error):
        
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

    return app

# =================== EXECUÇÃO PRINCIPAL ===================

if __name__ == '__main__':
    app = create_app()
    
    
    with app.app_context():
        
        print("\n⏳ Tentando conectar ao MariaDB e configurar as tabelas...")
        
        try:
            
            db.create_all()
            print("✅ Tabelas verificadas/criadas com sucesso.")
            
    
            populate_sample_data()
            print("📊 Dados de exemplo populados (se o banco estava vazio).")
            
        except Exception as e:
            
            print(f"❌ ERRO GRAVE DE CONEXÃO ou CONFIGURAÇÃO DO BANCO DE DADOS:")
            print(f"   Por favor, verifique se o XAMPP MySQL está ativo e se o banco 'medicamentosdb' foi criado.")
            print(f"   Detalhes: {e}")
        
            exit(1)
            
    print("\n==================================================")
    print("🏥 Farma Fácil API Flask + MariaDB INICIADA!")
    print(f"🔗 API disponível em: http://localhost:5000")
    print("📋 Health check: http://localhost:5000/api/health")
    print("==================================================")
        
    
    app.run(debug=True, host='0.0.0.0', port=5000)
