import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-40d6398718134128bd4ab2a8000a0649")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")


def _call_deepseek(system_prompt: str, user_prompt: str) -> str:
    """
    调用 DeepSeek Chat 接口的简单封装。
    """
    if not DEEPSEEK_API_KEY:
        print("⚠️ 警告：未配置 DEEPSEEK_API_KEY，使用本地模板回答")
        return ""

    url = f"{DEEPSEEK_API_BASE}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 256,
        "stream": False,
    }

    try:
        print(f"📡 正在调用 DeepSeek API: {url}")
        resp = requests.post(url, headers=headers, json=data, timeout=20)
        
        if resp.status_code != 200:
            print(f"❌ DeepSeek API 返回错误状态码: {resp.status_code}")
            print(f"响应内容: {resp.text}")
            return ""
        
        j = resp.json()
        
        if "choices" not in j or not j["choices"]:
            print("❌ DeepSeek API 返回的 choices 为空")
            return ""
        
        content = j["choices"][0]["message"]["content"]
        print(f"✅ DeepSeek API 调用成功，返回内容长度: {len(content)}")
        return content
        
    except requests.exceptions.Timeout:
        print("❌ DeepSeek API 请求超时（20秒）")
        return ""
    except requests.exceptions.ConnectionError as e:
        print(f"❌ DeepSeek API 连接失败: {e}")
        return ""
    except json.JSONDecodeError as e:
        print(f"❌ DeepSeek API 返回的不是有效 JSON: {e}")
        return ""
    except Exception as e:
        print(f"❌ DeepSeek API 调用出错: {type(e).__name__}: {e}")
        return ""


def generate_explanation(attraction_name, description, category, audience_type):
    """
    生成景点讲解：优先调用 DeepSeek，失败则走本地模板。
    """
    system_prompt = "你是华山景区的专业中文导游，用口语化、简洁的中文讲解景点，长度在80-120字左右。"
    user_prompt = f"""请为以下景点生成讲解词：

景点名称：{attraction_name}
景点类别：{category}
基本简介：{description}
目标游客人群：{audience_type}

要求：
- 根据不同人群调整讲解风格
- children: 用简单有趣的比喻和故事
- youth: 强调刺激性和打卡价值
- elderly: 强调安全提示和文化内涵
- all: 平衡介绍历史、自然和风险
- 不要超过120字"""

    ai_result = _call_deepseek(system_prompt, user_prompt)
    if ai_result:
        return ai_result

    # 兜底模板
    templates = {
        "children": f"{attraction_name}是华山最神奇的地方，这里有陡峭的悬崖、古老的故事和令人惊叹的景色。小朋友来这里就像在冒险，但要记住安全最重要哦！",
        "youth": f"{attraction_name}：{description}。这是年轻游客的打卡胜地，拍照效果绝赞！挑战自我的完美地点。",
        "elderly": f"{attraction_name}温馨提示：{description}。建议根据自身体力和身体状况量力而行，走走停停，欣赏美景，注意安全与休息。",
        "all": f"{attraction_name}：{description or '这是华山的重要景点之一。'}无论你是什么年龄，都能在这里找到属于自己的华山体验。",
    }
    return templates.get(audience_type, templates["all"])


def answer_huashan_question(question: str) -> str:
    """
    AI 问答：优先调用 DeepSeek，失败走本地知识库。
    """
    system_prompt = "你是华山景区的智能问答助手，用简洁、实用的中文回答游客的常见问题。回答长度控制在100-150字。"
    user_prompt = f"""游客提问：{question}

请基于以下信息回答：
- 华山常见登山方式：北路、西路、中路
- 推荐路线："西上北下"
- 高风险项目：长空栈道、鹞子翻身、苍龙岭
- 最佳季节：春秋季节

请给出实用的建议和安全提醒。"""

    ai_result = _call_deepseek(system_prompt, user_prompt)
    if ai_result:
        return ai_result

    # 本地知识库（兜底）
    qa_db = {
        "怎么登华山": "华山有多种登山方式：1) 北峰索道（最常见，时间短）；2) 西峰索道（景色好）；3) 中路步行（全程体验）。大多数游客选择'西上北下'路线，用时6-8小时。",
        "长空栈道": "长空栈道是华山最著名的险道，宽度不足1米，下面是千米悬崖。恐高症患者或有心血管疾病者强烈建议避免。需全程系安全带，手脚并用。",
        "体力一般": "体力一般的游客建议：1) 选择北峰索道往返或西峰索道+北峰索道；2) 避免长空栈道等高难度路段；3) 安排充足休息时间；4) 做好防晒和补水。",
        "看日出": "想看华山日出，建议前一天傍晚到达东峰附近，或者住在山上客栈。东峰是最佳观日出位置。记得带好头灯、防寒衣物和充足水源。",
        "一日游": "一日游推荐'西上北下'路线：8:00西峰索道上山→游览西峰、中峰、南峰→14:00到达北峰→16:00北峰索道下山。全程需要体力支持。",
        "儿童": "8岁以上儿童可考虑登华山，但要选择相对安全的路线（索道+北峰或简单路段）。做好防护措施，不要挑战高难度景点。",
        "票价": "华山门票约100-150元，北峰索道往返约60-80元，西峰索道约100-120元。具体价格以华山景区官方公告为准。",
        "天气": "华山天气多变，上山前检查天气预报。避免在恶劣天气登山，雷电天气必须下山。做好防晒和防雨准备。",
    }

    for key, answer in qa_db.items():
        if key in question:
            return answer

    return "感谢您的提问！建议您访问华山景区官网或拨打景区咨询电话，获取最新的游览信息、票价和安全提示。祝您游览愉快！"
