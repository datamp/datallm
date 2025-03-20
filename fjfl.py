#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:08:00 2025

@author: liun
"""

from openai import OpenAI
import json


def build_prompt(dept,duty,system,db, table, column, dtype, comment):
     prompt = f"""    
     你是一位资深数据安全专家，熟悉应急管理行业以及数据敏感等级划分。  
     应急管理部主要职责是组织编制国家应急总体预案和规划，指导各地区各部门应对突发事件工作，推动应急预案体系建设和预案演练。建立灾情报告系统并统一发布灾情，统筹应急力量建设和物资储备并在救灾时统一调度，组织灾害救助体系建设，指导安全生产类、自然灾害类应急救援，承担国家应对特别重大灾害指挥部工作。指导火灾、水旱灾害、地质灾害等防治。负责安全生产综合监督管理和工矿商贸行业安全生产监督管理等。公安消防部队、武警森林部队转制后，与安全生产等应急救援队伍一并作为综合性常备应急骨干力量，由应急管理部管理，实行专门管理和政策保障，采取符合其自身特点的职务职级序列和管理办法，提高职业荣誉感，保持有生力量和战斗力。应急管理部要处理好防灾和救灾的关系，明确与相关部门和地方各自职责分工，建立协调配合机制。
     以下是应急管理部定义的敏感等级标准：    
     - CORE：核心数据是指对领域、群体、区域具有较高覆盖或达到较高精度、较大规模、一定深度的重要数据，一旦被非法使用或共享，可能直接影响政治安全。主要包括：关系国家安全重点领域的数据，关系国民经济命脉、重要民生和重大公共利益的数据，经评估确定的其他数据    
     - IMPORTANT：重要数据是指特定领域、特定群体、特定区域或达到一定精度和规模的数据，一旦被泄露或篡改、损毁，可能直接危害国家安全、经济运行、社会稳定、公共健康和安全。仅影响组织自身或公民个体的数据，一般不作为重要数据    
     - FLG：一级一般数据遭到篡改、破坏、泄露或者非法获取、非法利用后，对公民、法人和其他组织的合法权益造成危害，但不危害国家安全、社会秩序和公共利益。在公民、法人和其它组织授权下可在一定范围内共享的数据。   
     - SLG：二级一般数据遭到篡改、破坏、泄露或者非法获取、非法利用后，不会对个人合法权益、组织合法权益造成危害。数据具有公共传播属性，可对外公开发布、转发传播。    
     现在有一条来自Hive库的字段元数据信息：    
     - 数据来源部门：{dept}
     - 部门职责：{duty}
     - 业务系统名称：{system}
     - 数据库名：{db}    
     - 表名：{table}    
     - 字段名：{column}    
     - 字段类型：{dtype}    
     - 字段注释：{comment}    
     请根据以上信息，判断此字段最合理的敏感等级，并简要说明你的理由。   
     输出JSON格式，形如：    
     {{      
       "level": "CORE/IMPORTANT/FLG/SLG",      
       "reason": "简要解释"    
       }}    
     """    
     return prompt

def call_llm_api(prompt):
    client = OpenAI(api_key="olloma", base_url="http://10.17.111.59:11434/v1")
    
    response = client.chat.completions.create(
        model="deepseek-r1:70b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={
        'type': 'json_object'
        },
        max_tokens = 1024,
        stream=False
    )
    
    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    dept = "危险化学品安全监督管理二司"
    duty = "承担化工（含石油化工）、医药、危险化学品经营安全监督管理工作,以及烟花爆竹生产经营、石油开采安全生产监督管理工作，依法监督检查相关行业生产经营单位贯彻落实安全生产法律法规和标准情况;承担危险化学品安全监督管理综合工作，组织指导危险化学品目录编制和国内危险化学品登记;承担海洋石油安全生产综合监督管理工作。"
    system = "危险化学品登记综合服务系统"
    db = "危险化学品登记综合服务系统"
    table = "企业证照信息"
    column = "business_license_code"
    dtype = "字符串型 C"
    comment = "危险化学品经营许可证编号	"
    prompt = build_prompt(dept,duty,system,db, table, column, dtype, comment)
    print(prompt)
    print("---------------------------")
    data_security_level = call_llm_api(prompt)
    print(data_security_level)

    
    
    