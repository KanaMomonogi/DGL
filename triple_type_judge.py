import re
import json
import itertools

#判断字符串s是否为数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

#根据实体名称返回类型
#input:△ABC
#output:三角形
def type_judge_by_name(e):
    #根据实体名称内容判断
    if e==None:
        return None
    if is_number(e):
        return "数值"
    if e.find("△")!=-1:
        return "三角形"
    if e.find("⊙")!=-1:
        return "圆"
    if e.find("∠")!=-1:
        return "角"
    if e.find("角")!=-1:
        return "角"
    if e.find("椭圆")!=-1:
        return "椭圆"
    if e.find("四边形")!=-1:
        return "四边形"
    if e.find("矩形")!=-1:
        return "四边形"
    if e.find("梯形")!=-1:
        return "四边形"
    if e.find("菱形")!=-1:
        return "四边形"
    if e.find("弦")!=-1:
        return "线段"
    if e.find("弧")!=-1:
        return "弧"

    #根据实体名称长度判断
    if len(e)==1:
        return "点"
    if len(e)==2:
        return "线段"
    if len(e)==3:
        return "三角形"
    if len(e)==4:
        return "四边形"

    #匹配均不成功
    return "未知"


#根据三元组关系返回实体类型
#input:(A,中点,BC)
#output:点,线段
def type_judge_by_relation(triple):
    e1,r,e2=triple
    if r=="点":
        return "点",None
    if r=="中点":
        return "点","线段"
    if r=="线段":
        return "线段",None
    if r=="直线":
        return "线段",None
    if r=="射线":
        return "线段",None
    if r=="延长线关系":
        return "线段",None
    if r=="角":
        return "角",None
    if r=="直角":
        return "角",None
    if r=="余角":
        return "角","角"
    if r=="补角":
        return "角","角"
    if r=="对顶角":
        return "角","角"
    if r=="同位角":
        return "角","角"
    if r=="内错角":
        return "角","角"
    if r=="同旁内角":
        return "角","角"
    if r=="三角形":
        return "三角形",None
    if r=="直角三角形":
        return "三角形",None
    if r=="等腰三角形":
        return "三角形",None
    if r=="等腰直角三角形":
        return "三角形",None
    if r=="等边三角形":
        return "三角形",None
    if r=="四边形":
        return "四边形",None
    if r=="平行四边形":
        return "四边形",None
    if r=="矩形":
        return "四边形",None
    if r=="菱形":
        return "四边形",None
    if r=="正方形":
        return "四边形",None
    if r=="梯形":
        return "四边形",None
    if r=="直角梯形":
        return "四边形",None
    if r=="圆心":
        return "点",type_judge_by_name(e2)
    if r=="位于上":
        return "点",type_judge_by_name(e2)
    if r=="相交":
        return type_judge_by_name(e1),type_judge_by_name(e2)
    if r=="垂直":
        return "线段","线段"
    if r=="平行":
        return "线段","线段"
    if r=="平分":
        return type_judge_by_name(e1),type_judge_by_name(e2)
    if r=="垂直平分":
        return type_judge_by_name(e1),type_judge_by_name(e2)
    if r=="全等":
        return type_judge_by_name(e1),type_judge_by_name(e2)
    if r=="相似":
        return type_judge_by_name(e1),type_judge_by_name(e2)
    if r=="重合":
        return type_judge_by_name(e1),type_judge_by_name(e2)
    if r=="角平分线":
        return "线段","角"
    if r=="三角形的高":
        return "线段","三角形"
    if r=="三角形的中线":
        return "线段","三角形"
    if r=="中位线":
        return "线段",type_judge_by_name(e2)
    if r=="三角形外角":
        return "角","三角形"
    if r=="重心":
        return "点","三角形"
    if r=="垂心":
        return "点","三角形"
    if r=="外心":
        return "点","三角形"
    if r=="外接圆":
        return type_judge_by_name(e1),"圆"
    if r=="内切圆":
        return type_judge_by_name(e1),"圆"
    if r=="对角线":
        return "线段",type_judge_by_name(e2)
    if r=="长度":
        return type_judge_by_name(e1),"数值"
    if r=="边长":
        return type_judge_by_name(e1),"数值"
    if r=="角度":
        return "角","数值"
    if r=="面积":
        return type_judge_by_name(e1),"数值"
    if r=="周长":
        return type_judge_by_name(e1),"数值"
    if r=="半径":
        return "线段",type_judge_by_name(e2)
    if r=="直径":
        return "线段",type_judge_by_name(e2)
    if r=="圆心角":
        return "角",type_judge_by_name(e2)
    if r=="圆周角":
        return "角",type_judge_by_name(e2)
    if r=="相切":
        return "线段","圆"
    if r=="弦":
        return "线段",type_judge_by_name(e2)
    if r=="弦切角":
        return "角",type_judge_by_name(e2)
    if r=="向量":
        return "向量",None
    if r=="值":
        return type_judge_by_name(e1),"数值"
    if r=="未知量":
        return type_judge_by_name(e1),"变量"