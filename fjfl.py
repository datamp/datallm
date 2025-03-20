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
     你是一位资深数据安全专家，熟悉XXXX行业以及数据敏感等级划分。  
     XXXXX主要职责是～。
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
    dept = "部门名称"
    duty = "部门职责"
    system = "系统名称"
    db = "数据库名称"
    table = "表说明"
    column = "字段名"
    dtype = "数据类型"
    comment = "字段注释"
    prompt = build_prompt(dept,duty,system,db, table, column, dtype, comment)
    print(prompt)
    print("---------------------------")
    data_security_level = call_llm_api(prompt)
    print(data_security_level)

    
    
    
