from flask import Blueprint, request, jsonify
from models import db, Medicamento, EstoqueExterno
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text # Para o health check

api_bp = Blueprint('api', __name__, url_prefix='/api')

# =====================================================================
# ENDPOINTS MEDICAMENTOS (CRUD)
# =====================================================================

@api_bp.route('/medicamentos', methods=['GET'])
def get_medicamentos():
    """Listar todos os medicamentos"""
    medicamentos = Medicamento.query.all()
    return jsonify([med.to_dict() for med in medicamentos])

@api_bp.route('/medicamentos/<int:id>', methods=['GET'])
def get_medicamento(id):
    """Buscar medicamento por ID"""
    
    medicamento = Medicamento.query.get_or_404(id, description="Medicamento não encontrado")
    return jsonify(medicamento.to_dict())

@api_bp.route('/medicamentos', methods=['POST'])
def create_medicamento():
    """Criar novo medicamento"""
    data = request.get_json()
    
    required_fields = ['nome', 'ean', 'laboratorio', 'principio_ativo', 'composicao', 
                       'dosagem', 'forma_administracao', 'para_que_serve', 'contraindicacao', 'armazenamento']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    try:
        
        medicamento = Medicamento(**data)
        db.session.add(medicamento)
        db.session.commit()
        return jsonify(medicamento.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Medicamento com este EAN já existe'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicamentos/<int:id>', methods=['PUT'])
def update_medicamento(id):
    """Atualizar medicamento existente"""
    medicamento = Medicamento.query.get_or_404(id, description="Medicamento não encontrado")
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(medicamento, key):
                setattr(medicamento, key, value)
        
        db.session.commit()
        return jsonify(medicamento.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Medicamento com este EAN já existe'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/medicamentos/<int:id>', methods=['DELETE'])
def delete_medicamento(id):
    """Excluir medicamento"""
    medicamento = Medicamento.query.get_or_404(id, description="Medicamento não encontrado")
    
    estoque_count = EstoqueExterno.query.filter_by(medicamento_id=id).count()
    if estoque_count > 0:
        return jsonify({
            'error': 'Não é possível excluir medicamento com registros de estoque. Exclua primeiro os registros de estoque.'
        }), 400
    
    try:
        db.session.delete(medicamento)
        db.session.commit()
        return jsonify({'message': 'Medicamento excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =====================================================================
# ENDPOINTS ESTOQUE EXTERNO (CRUD)
# =====================================================================

@api_bp.route('/estoque', methods=['GET'])
def get_estoque():
    """Listar todo o estoque com informações dos medicamentos"""
    estoque_list = EstoqueExterno.query.all()
    return jsonify([estoque.to_dict(include_medicamento=True) for estoque in estoque_list])

@api_bp.route('/estoque/medicamento/<int:medicamento_id>', methods=['GET'])
def get_estoque_por_medicamento(medicamento_id):
    """Buscar estoque por medicamento ID"""
    
    Medicamento.query.get_or_404(medicamento_id, description="Medicamento não encontrado")
    
    
    estoque_list = EstoqueExterno.query.filter_by(medicamento_id=medicamento_id).all()
    return jsonify([estoque.to_dict(include_medicamento=True) for estoque in estoque_list])

@api_bp.route('/estoque/farmacia/<string:farmacia_externa>', methods=['GET'])
def get_estoque_por_farmacia(farmacia_externa):
    """Buscar estoque por farmácia externa (usando string)"""
    
    estoque_list = EstoqueExterno.query.filter_by(farmacia_externa=farmacia_externa).all()
    return jsonify([estoque.to_dict(include_medicamento=True) for estoque in estoque_list])

@api_bp.route('/estoque/<int:id>', methods=['GET'])
def get_estoque_by_id(id):
    """Buscar registro de estoque por ID"""
    estoque = EstoqueExterno.query.get_or_404(id, description="Registro de estoque não encontrado")
    return jsonify(estoque.to_dict(include_medicamento=True))

@api_bp.route('/estoque', methods=['POST'])
def create_estoque():
    """Criar novo registro de estoque"""
    data = request.get_json()
    
    required_fields = ['medicamento_id', 'farmacia_externa', 'quantidade']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    
    Medicamento.query.get_or_404(data['medicamento_id'], description="Medicamento não encontrado")
    
    
    existing = EstoqueExterno.query.filter_by(
        medicamento_id=data['medicamento_id'],
        farmacia_externa=data['farmacia_externa']
    ).first()
    
    if existing:
        return jsonify({
            'error': 'Já existe registro de estoque para este medicamento nesta farmácia. Use PUT para atualizar.'
        }), 400
    
    try:
        estoque = EstoqueExterno(**data)
        db.session.add(estoque)
        db.session.commit()
        return jsonify(estoque.to_dict(include_medicamento=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/estoque/<int:id>', methods=['PUT'])
def update_estoque(id):
    """Atualizar registro de estoque"""
    estoque = EstoqueExterno.query.get_or_404(id, description="Registro de estoque não encontrado")
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(estoque, key) and key != 'id':
                setattr(estoque, key, value)
        
        db.session.commit()
        return jsonify(estoque.to_dict(include_medicamento=True))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/estoque/<int:id>', methods=['DELETE'])
def delete_estoque(id):
    """Excluir registro de estoque"""
    estoque = EstoqueExterno.query.get_or_404(id, description="Registro de estoque não encontrado")
    
    try:
        db.session.delete(estoque)
        db.session.commit()
        return jsonify({'message': 'Registro de estoque excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =====================================================================
# ENDPOINTS UTILITÁRIOS & HEALTH
# =====================================================================

@api_bp.route('/farmacias', methods=['GET'])
def get_farmacias():
    """Listar todas as farmácias com estoque"""
    
    farmacias = db.session.query(EstoqueExterno.farmacia_externa).distinct().all()
    return jsonify({'farmacias': [f[0] for f in farmacias]})

@api_bp.route('/', methods=['GET'])
def root():
    """Endpoint raiz da API"""
    return jsonify({
        'message': 'Farma Fácil API - Flask + MariaDB (XAMPP)',
        'version': '1.0.0',
        'status': 'OK',
        'endpoints': {
            'medicamentos': '/api/medicamentos',
            'estoque': '/api/estoque',
            'health': '/api/health'
        }
    })

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Check da saúde da API"""
    try:
        
        db.session.execute(text('SELECT 1')) 
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'error', 'error': str(e)}), 503
