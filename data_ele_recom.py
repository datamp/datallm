#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 10:07:09 2025

@author: liun
"""


from openai import OpenAI
import json
import pandas as pd 


def build_user_prompt(data_eles, column, dtype, comment):
     prompt = f"""
     以下是定义的XXXX数据元标准规范： 
{data_eles}
     现在有一条来自元数据管理平台的字段元数据信息：     
     - 字段名：{column}    
     - 字段类型：{dtype}    
     - 字段注释：{comment}    
     请根据以上信息，推荐此字段最合理的数据元，并简要说明你的理由。      
     """    
     return prompt
 
    
def build_system_prompt():
    character = """你是一位数据标准专家，熟悉XXXX行业以及数据标准管理,可以根据字段与数据元的语义相似度进行字段数据元推荐。  
     输出JSON格式，形如：    
     {      
       "data_ele": <推荐数据元>,      
       "reason": <简要解释>，
       "recom_degree":<一个百分比的数值，如：99.9999>
       
       }
     """
    return character

def call_llm_api(character,prompt):
    client = OpenAI(api_key="olloma", base_url="http://ip:/v1")
    response = client.chat.completions.create(
        model="deepseek-r1:70b",
        messages=[
            {"role": "system", "content": character},
            {"role": "user", "content": prompt}    
        ],
        max_tokens = 1024000,
        stream=False
    )
    rs = response.choices[0].message.content.split("</think>")[1].replace("\n","").replace("```","").replace("json","")
    print(rs)
    return json.loads(rs)


def call_llm_api_train(character,prompt,answer):
    client = OpenAI(api_key="olloma", base_url="http://ip:11434/v1")
    content = f"Answer:{answer}"
    response = client.chat.completions.create(
        model="deepseek-r1:70b",
        messages=[
            {"role": "system", "content": character},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": content},
        ],
        response_format={
        'type': 'json_object'
    },
        max_tokens = 512,
        stream=False
    )
    print(json.loads(response.choices[0].message.content))
    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    column = "business_license_code"
    dtype = "字符串型 C"
    comment = "统一社会信用代码"
    data_els_excel = pd.read_excel("data_element.xlsx")
    data_eles = []
    for index,row in data_els_excel.iterrows():
        cn_name = row["中文名称\n(*必填项)"]
        de_express = row["说明"]
        row_vale = f"     - {cn_name}"
        data_eles.append(row_vale)
    for index,row in data_els_excel.iterrows():
        cn_name = row["中文名称\n(*必填项)"]
        comment = "统一社会信用代码"
        character = build_system_prompt()
        prompt = build_user_prompt("\n".join(data_eles),column, dtype, cn_name)
        de = call_llm_api_train(character,prompt,cn_name)
        print(f"字段名称：{cn_name}")        
        try:
            data_ele = de["data_ele"]
            reason = de["reason"]
            recom_degree = de["recom_degree"]
            print(f"数据元：{data_ele}")
            print(f"简要描述：{reason}")
            print(f"匹配度：{recom_degree}")
        except Exception as err:
            print("未匹配到数据元："+str(err))
        print("--------------------------------")

