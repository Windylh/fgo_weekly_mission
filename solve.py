import json
import pulp
import os
import sys

path = os.path.abspath(os.path.dirname(__file__))

def generate_list(keywords, word_list, values):
    # print(values)
    a_temp = []
    for keyword in keywords:
        if keyword in word_list.get("place"):
            a_temp.append(1 if keyword in values.get("place") else 0)
        if keyword in word_list.get("mobs"):
            a_temp.append(int(values.get("mobs").get(keyword, 0)))
        if keyword in word_list.get("servant"):
            a_temp.append(int(values.get("servant").get(keyword, 0)))
    return a_temp


def solve_ilp(objective, constraints):
    # print(objective)
    # print(constraints)
    prob = pulp.LpProblem('LP1', pulp.LpMinimize)
    prob += objective
    for cons in constraints:
        prob += cons
    # print(prob)
    status = prob.solve()
    if status != 1:
        # print(status)
        return None
    else:
        result = {}
        for v in prob.variables():
            if v.varValue.real > 0:
                result[v] = int(v.varValue.real)
        result["total"] = int(pulp.value(prob.objective))
        return result


def solve(keywords, b_list):
    with open(path+"/stage.json", 'r') as f:
        stage = json.load(f)

    with open(path+"/keywords.json", "r") as f:
        word_list = json.load(f)

    name_list = []  # 章节-关卡
    c_list = []  # 关卡ap
    info_list = []  # 每个关卡对应keywords数量

    # 筛选出需要的关卡详情
    search_list = []
    key = list(stage.keys())
    values = list(stage.values())
    for keyword in keywords:
        if keyword in word_list.get("mobs"):
            for i in range(len(values)):
                if keyword in values[i].get('mobs', {}).keys() and key[i] not in search_list:
                    search_list.append(key[i])
                    info_list.append(generate_list(keywords, word_list, values[i]))
                    c_list.append(values[i].get('ap'))
                    name_list.append(f"{values[i].get('chapter_name')}-{list(stage.keys())[i]}")

        if keyword in word_list.get("servant"):
            for i in range(len(values)):
                if keyword in values[i].get('servant', {}).keys() and key[i] not in search_list:
                    search_list.append(key[i])
                    info_list.append(generate_list(keywords, word_list, values[i]))
                    c_list.append(values[i].get('ap'))
                    name_list.append(f"{values[i].get('chapter_name')}-{list(stage.keys())[i]}")

        if keyword in word_list.get("place"):
            for i in range(len(values)):
                if keyword in values[i].get('place', []) and key[i] not in search_list:
                    # print(key[i], search_list)
                    search_list.append(key[i])
                    info_list.append(generate_list(keywords, word_list, values[i]))
                    c_list.append(values[i].get('ap'))
                    name_list.append(f"{values[i].get('chapter_name')}-{list(stage.keys())[i]}")

    a_list = [list(i) for i in list(zip(*info_list))]  # 关卡特性个数

    V_NUM = len(c_list)
    # 变量，直接设置下限
    variables = [pulp.LpVariable(name_list[i], lowBound=0, cat=pulp.LpInteger) for i in range(0, V_NUM)]
    # 目标函数
    c = c_list
    objective = sum([c[i] * variables[i] for i in range(0, V_NUM)])
    # 约束条件
    constraints = []

    for i in range(len(a_list)):
        a = a_list[i]
        constraints.append(sum([a[j] * variables[j] for j in range(0, V_NUM)]) >= b_list[i])
    res = solve_ilp(objective, constraints)
    return res


if __name__ == "__main__":
    print(solve(["龙"], [3]))
