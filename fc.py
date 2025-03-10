
import os
import jieba
print(jieba.get_dict_file)  # 打印jieba的词典文件路径

jieba.load_userdict("./cut.txt")
text = "企业的信用评价扣分的标准内容。"
cuts =jieba.cut(text,cut_all=True)
print("|".join(cuts))


import difflib

def smart_match(field, data_elements):
    # 使用difflib库的get_close_matches函数来找到最接近的匹配
    cuts =jieba.cut(field,cut_all=True)
    matche_list = []
    for cut in cuts:
        matches = difflib.get_close_matches(cut, data_elements, n=3, cutoff=0.8)
        if matches:
            for matche in matches:
                matche_list.append(matche)
        else:
            pass
    return list(set(matche_list))


# 示例数据
fields = ["姓名", "年龄", "住址", "联系方式"]
data_elements = ["姓名", "住址","名字","联系电话","年龄", "详细地址", "电话","通讯方式","姓","名","名称","通讯地址","居住地址"]

# 进行智能匹配
for field in fields:
    match = smart_match(field, data_elements)
    if match:
        print(f"字段 '{field}' 匹配到数据元 '{match}'")
    else:
        print(f"字段 '{field}' 未找到匹配的数据元")

import hanlp

text = "我爱北京天安门"
# 分词


seg = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
print("分词: ", seg(text))

# 词性标注
pos = hanlp.load(hanlp.pretrained.pos.CTB5_POS_RNN_FASTTEXT_ZH)
print("词性标注: ", pos(text))
