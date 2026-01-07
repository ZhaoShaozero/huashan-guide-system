from flask import Blueprint, request, jsonify
from ai_service import generate_explanation, answer_huashan_question
import json

api_bp = Blueprint('api', __name__)

# 延迟导入以避免循环导入
def get_db_and_models():
    """延迟导入以避免循环导入"""
    from app import db
    from models import User, Attraction, Route, Explanation, Merchant, UserCheckIn
    return db, User, Attraction, Route, Explanation, Merchant, UserCheckIn

# ==================== 用户相关 API ====================

@api_bp.route('/users', methods=['POST'])
def create_user():
    """创建用户"""
    db, User, _, _, _, _, _ = get_db_and_models()
    data = request.get_json()
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': '用户已存在'}), 400
    user = User(
        username=data['username'],
        age_group=data.get('age_group'),
        fitness_level=data.get('fitness_level'),
        fear_of_heights=data.get('fear_of_heights', False),
        has_medical_condition=data.get('has_medical_condition', False)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息"""
    _, User, _, _, _, _, _ = get_db_and_models()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(user.to_dict())

# ==================== 景点相关 API ====================

@api_bp.route('/attractions', methods=['GET'])
def get_attractions():
    """获取所有景点"""
    _, _, Attraction, _, _, _, _ = get_db_and_models()
    attractions = Attraction.query.all()
    return jsonify([attr.to_dict() for attr in attractions])

@api_bp.route('/attractions/<int:attraction_id>', methods=['GET'])
def get_attraction(attraction_id):
    """获取单个景点详情"""
    _, _, Attraction, _, Explanation, _, _ = get_db_and_models()
    attraction = Attraction.query.get(attraction_id)
    if not attraction:
        return jsonify({'error': '景点不存在'}), 404
    result = attraction.to_dict()
    explanations = Explanation.query.filter_by(attraction_id=attraction_id).all()
    result['explanations'] = [exp.to_dict() for exp in explanations]
    return jsonify(result)

# ==================== 路线相关 API ====================

@api_bp.route('/routes', methods=['GET'])
def get_routes():
    """获取所有推荐路线"""
    _, _, _, Route, _, _, _ = get_db_and_models()
    routes = Route.query.all()
    return jsonify([route.to_dict() for route in routes])

@api_bp.route('/routes/recommend', methods=['POST'])
def recommend_route():
    """根据用户情况推荐路线"""
    _, _, _, Route, _, _, _ = get_db_and_models()
    data = request.get_json()
    fitness_level = data.get('fitness_level')
    fear_of_heights = data.get('fear_of_heights', False)
    has_medical_condition = data.get('has_medical_condition', False)
    
    if fear_of_heights or has_medical_condition or fitness_level == 'weak':
        route_name = '西峰索道上下'
    elif fitness_level == 'good' and not fear_of_heights:
        route_name = '西上北下（经典线路）'
    else:
        route_name = '北上西下'
    
    route = Route.query.filter_by(name=route_name).first()
    if not route:
        route = Route.query.first()
        if not route:
            return jsonify({'error': '暂无路线数据'}), 404
    
    return jsonify({
        'recommended_route': route.to_dict(),
        'reason': f'根据您的体力情况（{fitness_level}）和偏好，推荐此路线'
    })

@api_bp.route('/routes/<int:route_id>', methods=['GET'])
def get_route(route_id):
    """获取单个路线详情"""
    _, _, Attraction, Route, _, _, _ = get_db_and_models()
    route = Route.query.get(route_id)
    if not route:
        return jsonify({'error': '路线不存在'}), 404
    result = route.to_dict()
    attraction_ids = result['attractions']
    attractions = []
    for attr_id in attraction_ids:
        attr = Attraction.query.get(attr_id)
        if attr:
            attractions.append(attr.to_dict())
    result['attraction_details'] = attractions
    return jsonify(result)

# ==================== AI 讲解 API ====================

@api_bp.route('/ai/explain/<int:attraction_id>', methods=['POST'])
def get_ai_explanation(attraction_id):
    """获取 AI 生成的景点讲解"""
    print(f"📌 收到景点讲解请求: attraction_id={attraction_id}")
    _, _, Attraction, _, _, _, _ = get_db_and_models()
    attraction = Attraction.query.get(attraction_id)
    if not attraction:
        print(f"❌ 景点 {attraction_id} 不存在")
        return jsonify({'error': '景点不存在'}), 404
    
    data = request.get_json()
    audience_type = data.get('audience_type', 'all')
    print(f"📝 生成讲解词: {attraction.name}, audience={audience_type}")
    
    explanation = generate_explanation(
        attraction_name=attraction.name,
        description=attraction.description,
        category=attraction.category,
        audience_type=audience_type
    )
    
    print(f"✅ 讲解词生成完成，长度: {len(explanation)}")
    return jsonify({
        'attraction_id': attraction_id,
        'attraction_name': attraction.name,
        'audience_type': audience_type,
        'explanation': explanation
    })

@api_bp.route('/ai/ask', methods=['POST'])
def ask_huashan():
    """AI 智能问答"""
    print(f"📌 收到 AI 问答请求")
    data = request.get_json()
    question = data.get('question', '')
    print(f"❓ 用户问题: {question}")
    
    if not question:
        print(f"❌ 问题为空")
        return jsonify({'error': '问题不能为空'}), 400
    
    print(f"🤖 调用 AI 服务生成回答...")
    answer = answer_huashan_question(question)
    print(f"✅ 回答生成完成，长度: {len(answer)}")
    
    return jsonify({
        'question': question,
        'answer': answer
    })

# ==================== 商家信息 API ====================

@api_bp.route('/merchants', methods=['GET'])
def get_merchants():
    """获取商家列表"""
    _, _, _, _, _, Merchant, _ = get_db_and_models()
    category = request.args.get('category')
    query = Merchant.query
    if category:
        query = query.filter_by(category=category)
    merchants = query.all()
    return jsonify([m.to_dict() for m in merchants])

# ==================== 用户打卡 API ====================

@api_bp.route('/checkin', methods=['POST'])
def create_checkin():
    """用户打卡"""
    db, _, _, _, _, _, UserCheckIn = get_db_and_models()
    data = request.get_json()
    checkin = UserCheckIn(
        user_id=data.get('user_id'),
        attraction_id=data.get('attraction_id'),
        notes=data.get('notes', ''),
        rating=data.get('rating')
    )
    db.session.add(checkin)
    db.session.commit()
    return jsonify(checkin.to_dict()), 201

@api_bp.route('/checkins/<int:user_id>', methods=['GET'])
def get_user_checkins(user_id):
    """获取用户的打卡记录"""
    _, _, _, _, _, _, UserCheckIn = get_db_and_models()
    checkins = UserCheckIn.query.filter_by(user_id=user_id).all()
    return jsonify([c.to_dict() for c in checkins])

# ==================== 安全检查 API ====================

@api_bp.route('/safety-check', methods=['POST'])
def safety_check():
    """对于危险景点的安全检查"""
    _, User, Attraction, _, _, _, _ = get_db_and_models()
    data = request.get_json()
    attraction_id = data.get('attraction_id')
    user_id = data.get('user_id')
    
    attraction = Attraction.query.get(attraction_id)
    user = User.query.get(user_id) if user_id else None
    
    if not attraction:
        return jsonify({'error': '景点不存在'}), 404
    
    warnings = []
    if user:
        if user.fear_of_heights and attraction.difficulty_level >= 3:
            warnings.append('您可能恐高，该路段较为陡峭，请谨慎')
        if user.has_medical_condition and attraction.safety_level in ['高危', '极端危险']:
            warnings.append('您有心脏病/高血压等疾病，建议避免此危险路段')
        if user.fitness_level == 'weak' and attraction.estimated_time > 100:
            warnings.append('该路段较长且陡峭，您的体力可能不足，请评估')
    
    return jsonify({
        'attraction_id': attraction_id,
        'attraction_name': attraction.name,
        'safety_level': attraction.safety_level,
        'warnings': warnings,
        'can_proceed': len(warnings) == 0,
        'tips': attraction.tips or f'{attraction.name} 的安全提示：需要注意脚下，手脚并用。'
    })

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'message': '后端服务运行正常'
    }), 200