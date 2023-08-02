import re
import json
import itertools
from triple_type_judge import *

'''
从json数据中得到三元组list
input:json数组格式的字符串
output:规范化后的三元组list
'''
def getTripleFromJson(jsonString):
    triplelistString = json.loads(jsonString).get("relations")
    tripleTuplelist = []
    for t in triplelistString:
        tripleTuplelist.append((t.get("entity1"),t.get("relationType"),t.get("entity2")))
    print("三元组Tuple列表为：",tripleTuplelist)
    return tripleTuplelist

'''
处理等式三元组，生成规范三元组。
input:等式字符串
ouput:多个规范三元组
目前已处理格式：
∠1=∠2=∠3
待处理格式：
∠1=∠2=90°
......
'''
def genarateByequation(e1:str):
    expr_list = e1.split("=")
    entities=[]
    entitiesAll= []
    entity_types = {}
    std_tuples = []
    for expr in expr_list:
        tmp_lst = re.split(r"[\+-/*]", expr)
        entities.append(tmp_lst)
        entitiesAll.extend(tmp_lst)
    #去重
    entitiesAll = list(set(entitiesAll))
    print(entities)
    for entity in entitiesAll:
        entity_types[entity] = type_judge_by_name(entity)
    #是否都为“单一实体的表达式”
    if all( len(entitylst) == 1 for entitylst in entities):
        #全是线段或角
        if all( v == "角" or "线段" for k,v in entity_types):
            for combination in itertools.combinations(entitiesAll,2):
                std_tuples.append((combination[0],"相等",combination[1]))
    return std_tuples