import random
import sys
import time


# ================================
# 状态定义
# ================================
state = {
    "cash": 0,
    "supply": 0,
    "brand": 0,
    "team": 0,
    "growth": 0,
    "risk": 0,
    "history": []
}

macro = {
    "usdRate": 7.10,              # 汇率
    "tariff": 10,                 # %
    "inflation": 2,               # %
    "interestRate": 3.5,          # %
    "externalSupplyRisk": 10,     # 0-100
    "consumerConfidence": 80,     # 0-100
    "geoTension": 10              # 地缘紧张度
}


# ================================
# 剧情关卡（11关）
# ================================
questions = [
    {
        "id": 1,
        "text": "毕业后，你想干什么？",
        "options": {
            "A": ("去会计师事务所上班（稳定工作）", {"cash": 10, "growth": 5, "risk": -5}),
            "B": ("环球旅行寻找灵感", {"cash": -10, "growth": 10, "risk": 5, "brand": 5}),
            "C": ("在家写商业计划书", {"cash": -5, "growth": 5}),
            "D": ("随便混几年", {"growth": -5, "risk": -5})
        }
    },
    {
        "id": 2,
        "text": "你想做跑鞋生意，要不要去日本谈代理？",
        "options": {
            "A": ("立刻飞日本", {"cash": -10, "growth": 10, "risk": 5, "brand": 5}),
            "B": ("写邮件等回复", {"risk": -5, "growth": -5}),
            "C": ("不去", {"growth": -10}),
            "D": ("借钱飞日本", {"cash": -20, "growth": 15, "risk": 10, "brand": 5})
        }
    },
    {
        "id": 3,
        "text": "供应商问你公司多大？",
        "options": {
            "A": ("老实说只有你一个人", {"supply": -5, "brand": -2, "risk": -5}),
            "B": ("模糊回答", {"supply": 5, "risk": 5, "brand": 2}),
            "C": ("吹牛：我们是大型分销商", {"supply": 10, "risk": 15, "brand": 5}),
            "D": ("反问并展示专业度", {"supply": 5, "growth": 5, "brand": 3})
        }
    },
    {
        "id": 4,
        "text": "第一批鞋到美国了，你怎么卖？",
        "options": {
            "A": ("校园地推", {"brand": 15, "cash": 5, "growth": 10, "team": 5, "risk": -5}),
            "B": ("铺货给零售店", {"cash": 10, "supply": 5, "brand": 5}),
            "C": ("让朋友帮忙卖", {"cash": 5, "team": 5, "risk": 5}),
            "D": ("砸广告推广", {"cash": -15, "brand": 15, "risk": 5})
        }
    },
    {
        "id": 5,
        "text": "销量起来，但现金紧张，怎么办？",
        "options": {
            "A": ("银行贷款", {"cash": 30, "risk": 10, "supply": 10, "brand": 5, "growth": 5}),
            "B": ("向父母借钱", {"cash": 15, "team": -5, "risk": 5}),
            "C": ("刷信用卡", {"cash": 20, "risk": 20}),
            "D": ("放慢扩张", {"growth": -10, "risk": -10, "supply": -5})
        }
    },
    {
        "id": 6,
        "text": "Johnson 天才型销售，怎么管？",
        "options": {
            "A": ("放手让他冲", {"brand": 15, "team": 10, "cash": 10, "growth": 10, "risk": 5, "supply": -5}),
            "B": ("严格KPI", {"team": -5, "cash": 5, "growth": 5, "risk": -5}),
            "C": ("重点客户 + 有限放权", {"brand": 10, "team": 5, "cash": 5, "growth": 5}),
            "D": ("开除", {"brand": -10, "team": -5, "growth": -5})
        }
    },
    {
        "id": 7,
        "text": "供应链断货风险，你怎么办？",
        "options": {
            "A": ("施压供应商", {"supply": -5, "risk": 5, "brand": -2}),
            "B": ("新增供应商", {"supply": 20, "risk": -20, "cash": -10, "brand": 10, "team": 5, "growth": 10}),
            "C": ("等待", {"supply": -15, "cash": -5, "risk": 5}),
            "D": ("公开吐槽供应商", {"brand": -20, "risk": 20})
        }
    },
    {
        "id": 8,
        "text": "竞争对手抄袭，怎么办？",
        "options": {
            "A": ("新款迭代", {"brand": 10, "cash": -5, "growth": 10}),
            "B": ("打官司", {"cash": -20, "brand": 10, "risk": -5, "team": 5, "growth": 5}),
            "C": ("降价竞争", {"cash": -10, "brand": -10, "risk": 10}),
            "D": ("讲品牌故事", {"brand": 15, "cash": -5, "growth": 5})
        }
    },
    {
        "id": 9,
        "text": "要不要扩展品类？",
        "options": {
            "A": ("继续深耕跑鞋", {"risk": -15, "cash": 10, "team": 5, "supply": 5, "growth": -5}),
            "B": ("做篮球鞋", {"growth": 15, "cash": -10, "risk": 10, "brand": 10}),
            "C": ("做服装", {"brand": 10, "cash": -5, "risk": 5}),
            "D": ("全线开火", {"growth": 20, "cash": -20, "risk": 20})
        }
    },
    {
        "id": 10,
        "text": "欧洲进入，怎么做？",
        "options": {
            "A": ("小规模试水", {"growth": 10, "cash": -10, "risk": 5, "brand": 5}),
            "B": ("大规模进入", {"growth": 20, "cash": -20, "risk": 20, "brand": 15}),
            "C": ("当地代理", {"supply": 10, "risk": -10, "brand": 15, "growth": 10, "team": 5}),
            "D": ("暂缓", {"growth": -5, "risk": -5})
        }
    },
    {
        "id": 11,
        "text": "投资人问：要不要现在上市？",
        "options": {
            "A": ("马上上市", {"cash": 50, "risk": 20, "brand": 10, "growth": 15}),
            "B": ("再等一年", {"risk": -10, "brand": 10, "team": 10, "growth": 5, "supply": 5}),
            "C": ("再融一轮私募", {"cash": 20, "risk": 5, "growth": 5}),
            "D": ("拒绝上市", {"risk": -5, "growth": -5})
        }
    }
]


# ================================
# 宏观事件（概率触发，条件 + 权重）
# ================================
macro_events = [
    {
        "id": "oil-war",
        "name": "中东局势升级，油价暴涨",
        "desc": "油价飙升 → 海运成本大增",
        "weight": 3,
        "condition": lambda r: True,
        "effects": {
            "stats": {"cash": -5, "supply": -5, "risk": 5},
            "macro": {"inflation": 0.5, "externalSupplyRisk": 8, "geoTension": 5}
        }
    },
    {
        "id": "fed-hike",
        "name": "美联储激进加息",
        "desc": "融资成本提高 + 消费信心下降",
        "weight": 3,
        "condition": lambda r: r >= 3,
        "effects": {
            "stats": {"cash": -5, "growth": -5, "risk": 3},
            "macro": {"interestRate": 0.75, "consumerConfidence": -5}
        }
    },
    {
        "id": "fed-cut",
        "name": "美联储意外降息",
        "desc": "资金成本降低 + 消费改善",
        "weight": 2,
        "condition": lambda r: macro["interestRate"] > 3.5,
        "effects": {
            "stats": {"cash": 5, "growth": 5},
            "macro": {"interestRate": -0.5, "consumerConfidence": 5}
        }
    },
    {
        "id": "tariff-up",
        "name": "中美贸易摩擦升级",
        "desc": "关税上升 → 海外利润下降",
        "weight": 3,
        "condition": lambda r: r >= 5,
        "effects": {
            "stats": {"growth": -5, "brand": -5, "risk": 5},
            "macro": {"tariff": 5, "geoTension": 10, "consumerConfidence": -3}
        }
    },
    {
        "id": "tariff-relief",
        "name": "中美阶段性缓和",
        "desc": "关税回落 → 地缘风险下降",
        "weight": 2,
        "condition": lambda r: macro["tariff"] >= 15,
        "effects": {
            "stats": {"growth": 5, "brand": 5},
            "macro": {"tariff": -5, "geoTension": -8, "consumerConfidence": 4}
        }
    },
    {
        "id": "port-strike",
        "name": "港口罢工",
        "desc": "货物滞留港口，供应链延误",
        "weight": 3,
        "condition": lambda r: r >= 4,
        "effects": {
            "stats": {"cash": -8, "supply": -10, "risk": 5, "brand": -3},
            "macro": {"externalSupplyRisk": 10}
        }
    },
    {
        "id": "sports-boom",
        "name": "全球体育热潮",
        "desc": "运动鞋需求快速上涨",
        "weight": 4,
        "condition": lambda r: state["brand"] >= 10,
        "effects": {
            "stats": {"cash": 10, "growth": 12, "brand": 8},
            "macro": {"consumerConfidence": 10}
        }
    },
    {
        "id": "black-swan",
        "name": "黑天鹅：运河堵塞",
        "desc": "运输中断 → 供应链冻结",
        "weight": 1,
        "condition": lambda r: r >= 6,
        "effects": {
            "stats": {"cash": -12, "supply": -15, "risk": 10},
            "macro": {"externalSupplyRisk": 15, "inflation": 0.8, "geoTension": 5}
        }
    }
]


# ================================
# 工具函数
# ================================
def apply_effects(effects):
    for k, v in effects.items():
        state[k] += v


def is_bankrupt():
    if state["cash"] < -10:
        return "现金流崩溃"
    if state["supply"] < -20:
        return "供应链断裂"
    if state["team"] < -15:
        return "团队崩塌"
    return None


def maybe_macro_event(round_num):
    base_prob = 0.45
    if macro["geoTension"] >= 40 or macro["externalSupplyRisk"] >= 40:
        base_prob += 0.15

    if random.random() > base_prob:
        return None

    possible = [ev for ev in macro_events if ev["condition"](round_num)]
    if not possible:
        return None

    # 加权随机
    total_weight = sum(ev["weight"] for ev in possible)
    r = random.uniform(0, total_weight)
    for ev in possible:
        r -= ev["weight"]
        if r <= 0:
            return ev

    return possible[-1]


def apply_macro_event(ev):
    sdelta = ev["effects"].get("stats", {})
    mdelta = ev["effects"].get("macro", {})

    for k, v in sdelta.items():
        state[k] += v

    for k, v in mdelta.items():
        macro[k] += v

    print(f"\n⚠️【宏观事件触发】{ev['name']}")
    print(f"📌 {ev['desc']}")
    print(f"→ 影响（stats）：{sdelta}")
    print(f"→ 影响（macro）：{mdelta}\n")


# ================================
# 结局判断
# ================================
def evaluate_ending():
    death = is_bankrupt()
    macro_risk = (
        macro["externalSupplyRisk"] * 0.3
        + macro["geoTension"] * 0.3
        + macro["inflation"] * 0.5
    )
    effective_risk = state["risk"] + macro_risk * 0.2

    power = (
        state["brand"] * 1.5 +
        state["growth"] * 1.2 +
        state["supply"] * 1.0 +
        state["team"] * 1.0 +
        state["cash"] * 0.8 -
        effective_risk * 0.5
    )

    if death:
        return "【结局：倒在周期中】", f"原因：{death}"

    if power >= 230:
        return "【结局：超越耐克】", "你利用所有宏观与微观窗口期，成为世界第一运动品牌。"
    elif power >= 190:
        return "【结局：全球运动巨头】", "你顶住了战争、关税、利率冲击，实现全球扩张。"
    elif power >= 135:
        return "【结局：中国顶级品牌】", "类似安踏，成功穿越周期。"
    elif power >= 90:
        return "【结局：区域品牌】", "你在部分市场成功，但未成全球化。"
    elif power >= 50:
        return "【结局：生存者】", "没有死，但也没有做大。"
    else:
        return "【结局：周期夹缝中生存】", "你被宏观与微观双重挤压，只能勉强活着。"


# ================================
# 主流程
# ================================
def play_game():
    print("=======================================")
    print("     ShoeDog 创业模拟 2.0（Python版）")
    print("         宏观经济 + 黑天鹅系统")
    print("=======================================\n")

    for idx, q in enumerate(questions):
        print(f"\n第 {q['id']} 关：{q['text']}\n")

        for key, (text, eff) in q["options"].items():
            print(f"  {key}. {text}")

        choice = ""
        while choice not in q["options"]:
            choice = input("\n请输入你的选择（A/B/C/D）：").upper()

        _, effects = q["options"][choice]
        apply_effects(effects)

        print(f"👉 选择 {choice}，效果：{effects}")

        # 检查是否提前死亡
        death = is_bankrupt()
        if death:
            print("\n💀 你倒下了！")
            print("原因：", death)
            break

        # 触发宏观事件
        ev = maybe_macro_event(q["id"])
        if ev:
            apply_macro_event(ev)

    # 最终结局
    title, desc = evaluate_ending()
    print("\n============================")
    print(title)
    print(desc)
    print("\n最终状态：", state)
    print("宏观环境：", macro)


if __name__ == "__main__":
    play_game()
