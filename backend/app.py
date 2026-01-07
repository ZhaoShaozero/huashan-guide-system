# backend/app.py
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db

load_dotenv()


def create_app():
    app = Flask(__name__)
    
    # 配置 CORS - 允许来自所有域名的请求
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # 允许所有域名
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 延迟导入，避免循环
    from routes import api_bp
    from models import Attraction, Route

    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        if Attraction.query.first() is None:
            init_attractions()
        if Route.query.first() is None:
            init_routes()

    return app


def init_attractions():
    from models import Attraction
    from extensions import db

    attractions = [
        Attraction(
            name='西峰（莲花峰）',
            description='华山西峰，又名莲花峰，是华山五峰之一，以雄奇险峻著称。',
            category='主峰',
            latitude=34.4746,
            longitude=110.0974,
            altitude=2096,
            difficulty_level=3,
            estimated_time=120,
            safety_level='高危',
            image_url=''
        ),
        Attraction(
            name='东峰（朝阳峰）',
            description='东峰又名朝阳峰，是观看日出的最佳地点之一。',
            category='主峰',
            latitude=34.4821,
            longitude=110.1076,
            altitude=2096,
            difficulty_level=2,
            estimated_time=100,
            safety_level='高危',
            image_url=''
        ),
        Attraction(
            name='南峰（落雁峰）',
            description='南峰又名落雁峰，海拔约2155米，为华山最高峰。',
            category='主峰',
            latitude=34.4701,
            longitude=110.1016,
            altitude=2155,
            difficulty_level=3,
            estimated_time=150,
            safety_level='极端危险',
            image_url=''
        ),
        Attraction(
            name='北峰（云台峰）',
            description='北峰海拔较低，多数游客选择在此乘索道上下山。',
            category='主峰',
            latitude=34.4890,
            longitude=110.1015,
            altitude=1615,
            difficulty_level=1,
            estimated_time=60,
            safety_level='较安全',
            image_url=''
        ),
        Attraction(
            name='中峰（玉女峰）',
            description='中峰又名玉女峰，位于南北两峰之间，传说玉女曾在此修行。',
            category='主峰',
            latitude=34.4780,
            longitude=110.1010,
            altitude=2042,
            difficulty_level=2,
            estimated_time=80,
            safety_level='中等',
            image_url=''
        ),
        Attraction(
            name='长空栈道',
            description='贴壁木板栈道，下临深渊，是华山著名高风险项目。',
            category='险道',
            latitude=34.4710,
            longitude=110.0995,
            altitude=2000,
            difficulty_level=4,
            estimated_time=30,
            safety_level='极端危险',
            image_url=''
        ),
        Attraction(
            name='鹞子翻身',
            description='需贴壁攀爬铁索而上，道路狭窄陡峭，极具挑战性。',
            category='险道',
            latitude=34.4760,
            longitude=110.1040,
            altitude=1980,
            difficulty_level=4,
            estimated_time=20,
            safety_level='极端危险',
            image_url=''
        ),
        Attraction(
            name='苍龙岭',
            description='两侧悬崖，中间狭窄岭脊，是中路上非常刺激的一段路。',
            category='险道',
            latitude=34.4820,
            longitude=110.1050,
            altitude=1700,
            difficulty_level=3,
            estimated_time=45,
            safety_level='高危',
            image_url=''
        ),
        Attraction(
            name='玉泉院',
            description='北路登山传统起点，道教古观，环境清幽。',
            category='文化建筑',
            latitude=34.4950,
            longitude=110.0900,
            altitude=600,
            difficulty_level=0,
            estimated_time=10,
            safety_level='安全',
            image_url=''
        ),
    ]
    for a in attractions:
        db.session.add(a)
    db.session.commit()


def init_routes():
    from models import Route
    from extensions import db
    import json

    routes = [
        Route(
            name='西上北下（经典一日游）',
            description='西峰索道上山，经南峰、中峰、东峰，最后北峰索道下山。',
            difficulty='medium',
            estimated_duration=480,
            attractions=json.dumps([1, 3, 5, 2, 4]),
            recommended_for='普通游客',
            cable_car_usage='西峰上山，北峰下山',
            image_url=''
        ),
        Route(
            name='西峰索道上下（轻松路线）',
            description='西峰索道往返，适合体力一般或中老年游客。',
            difficulty='easy',
            estimated_duration=240,
            attractions=json.dumps([1, 3]),
            recommended_for='老年人',
            cable_car_usage='西峰往返',
            image_url=''
        ),
        Route(
            name='北上西下（挑战路线）',
            description='北峰上山，经苍龙岭等路段，最后西峰索道下山，体力要求较高。',
            difficulty='hard',
            estimated_duration=540,
            attractions=json.dumps([4, 8, 3, 1]),
            recommended_for='年轻人',
            cable_car_usage='北峰上，西峰下',
            image_url=''
        ),
    ]
    for r in routes:
        db.session.add(r)
    db.session.commit()


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=15500)
