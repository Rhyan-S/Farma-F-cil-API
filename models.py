# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship 
from sqlalchemy import text # Necessário para o Health Check
import uuid 

db = SQLAlchemy()

# =====================================================================
# MODELO 1: Medicamento (Espelha a tabela 'medicamentos')
# =====================================================================

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    nome = db.Column(db.String(255), nullable=False)
    ean = db.Column(db.String(20), nullable=False, unique=True) # EAN agora é UNICO
    laboratorio = db.Column(db.String(255), nullable=False)
    principio_ativo = db.Column(db.String(255), nullable=False)
    composicao = db.Column(db.Text, nullable=False)
    
    dosagem = db.Column(db.String(50), nullable=False)
    forma_administracao = db.Column(db.String(50), nullable=False)
    para_que_serve = db.Column(db.Text, nullable=False)
    contraindicacao = db.Column(db.Text, nullable=False)
    armazenamento = db.Column(db.Text, nullable=False)
    
    estoque_externo = relationship('EstoqueExterno', backref='medicamento_ref', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Retorna o objeto como um dicionário JSON serializável."""
        return {
            'id': self.id,
            'nome': self.nome,
            'ean': self.ean,
            'laboratorio': self.laboratorio,
            'principio_ativo': self.principio_ativo,
            'composicao': self.composicao,
            'dosagem': self.dosagem,
            'forma_administracao': self.forma_administracao,
            'para_que_serve': self.para_que_serve,
            'contraindicacao': self.contraindicacao,
            'armazenamento': self.armazenamento
        }

# =====================================================================
# MODELO 2: EstoqueExterno (Espelha a tabela 'estoqueexterno')
# =====================================================================

class EstoqueExterno(db.Model):
    __tablename__ = 'estoqueexterno'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)
    farmacia_externa = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_medicamento=False):
        """Retorna o objeto como um dicionário, com opção de incluir dados do medicamento."""
        result = {
            'id': self.id,
            'medicamento_id': self.medicamento_id,
            'farmacia_externa': self.farmacia_externa,
            'quantidade': self.quantidade,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }
        
    
        if include_medicamento and self.medicamento_ref:
            result['medicamento'] = self.medicamento_ref.to_dict()
            
        return result

# =====================================================================
# FUNÇÃO HELPER: Popula dados de exemplo
# =====================================================================

def populate_sample_data():
    """Popula banco de dados com dados de exemplo (se vazio)"""
    
    # Se a tabela medicamentos já tiver dados, não faz nada
    if Medicamento.query.count() > 0:
        return
    
    # Dados de Exemplo
    sample_medicamentos = [
        # primeiro registro SQL
        {
            'nome': 'Paracetamol',
            'ean': '7891000001234',
            'laboratorio': 'Farmaceutica XYZ',
            'principio_ativo': 'Paracetamol',
            'composicao': 'Cada comprimido contém 500mg de Paracetamol',
            'dosagem': '500mg',
            'forma_administracao': 'VO',
            'para_que_serve': 'O Paracetamol é um analgésico e antipirético utilizado para aliviar dores leves a moderadas e reduzir febre.',
            'contraindicacao': 'Contraindicado para pacientes com insuficiência hepática grave.',
            'armazenamento': 'Conservar em temperatura ambiente, abaixo de 30°C, e proteger da umidade.'
        },
        # Novo registro
        {
            'nome': 'Dipirona',
            'ean': '7891234567891',
            'laboratorio': 'Medley',
            'principio_ativo': 'Dipirona Sódica',
            'composicao': 'Dipirona Sódica 500mg + Excipientes',
            'dosagem': '500mg',
            'forma_administracao': 'Comprimido',
            'para_que_serve': 'Analgésico e antipirético para dores intensas.',
            'contraindicacao': 'Contraindicado para alérgicos a pirazolonas.',
            'armazenamento': 'Temperatura ambiente.'
        },
        # Outro registro
        {
            'nome': 'Ibuprofeno',
            'ean': '7891234567892',
            'laboratorio': 'Eurofarma',
            'principio_ativo': 'Ibuprofeno',
            'composicao': 'Ibuprofeno 600mg + Excipientes',
            'dosagem': '600mg',
            'forma_administracao': 'Cápsula',
            'para_que_serve': 'Anti-inflamatório, analgésico e antipirético.',
            'contraindicacao': 'Úlcera péptica ativa.',
            'armazenamento': 'Temperatura ambiente, local seco.'
        }
    ]
    
    medicamentos_criados = []
    
    
    for med_data in sample_medicamentos:
    
        medicamento = Medicamento(**med_data)
        db.session.add(medicamento)
        medicamentos_criados.append(medicamento)
    
    db.session.commit()
    

    farmacias = ['FARM-A', 'FARM-B']
    
    for i, medicamento in enumerate(medicamentos_criados):
        for farmacia in farmacias:
            estoque = EstoqueExterno(
                medicamento_id=medicamento.id,
                farmacia_externa=farmacia,
                quantidade=(i + 1) * 50
            )
            db.session.add(estoque)
    
    db.session.commit()