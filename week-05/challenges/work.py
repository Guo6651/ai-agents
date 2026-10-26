"""W5 综合选做：按合同完成函数，使用 challenges 中的公开测试验收。"""

"""第一题"""
def summarize_values(values):
    """整理普通整数列表；不修改输入。

    返回 {"unique": 首次出现顺序的去重列表,
          "counts": 每个整数的出现次数字典,
          "repeated": 出现次数大于 1 的整数集合}。
    空输入返回 {"unique": [], "counts": {}, "repeated": set()}。
    每次调用产生独立结果，结果中的列表、字典、集合可以单独修改。
    """
    order_list = []      
    num_counts = {}      
    duplicate_set = set()

    for num in values:
        if num in num_counts:
            num_counts[num] += 1
            duplicate_set.add(num)
        else:
            num_counts[num] = 1
            order_list.append(num)

    return {
        "unique": order_list,
        "counts": num_counts,
        "repeated": duplicate_set
    }
    # ===== 实现代码结束 =====

# ===== 下面是测试代码，放在函数外面 =====
# 注意：这行代码要和 def 开头对齐（不要缩进），否则会报错
if __name__ == "__main__":
    my_data = [5, 2, 5, 8, -2, 2, 5]
    print("我的输入 my_data:", my_data)

    my_result = summarize_values(my_data)
    print("我的输出结果:", my_result)

    expected = {
        "unique": [5, 2, 8, -2],
        "counts": {5: 3, 2: 2, 8: 1, -2: 1},
        "repeated": {2, 5}
    }

    assert my_result == expected
    assert my_data == [5, 2, 5, 8, -2, 2, 5] 




def summarize_values(values):
    """整理普通整数列表；不修改输入。

    返回 {"unique": 首次出现顺序的去重列表,
          "counts": 每个整数的出现次数字典,
          "repeated": 出现次数大于 1 的整数集合}。
    空输入返回 {"unique": [], "counts": {}, "repeated": set()}。
    每次调用产生独立结果，结果中的列表、字典、集合可以单独修改。
    """
    order_list = []      
    num_counts = {}      
    duplicate_set = set()

    for num in values:
        if num in num_counts:
            num_counts[num] += 1
            duplicate_set.add(num)
        else:
            num_counts[num] = 1
            order_list.append(num)

    return {
        "unique": order_list,
        "counts": num_counts,
        "repeated": duplicate_set
    }


# ===== 下面是测试代码，放在函数外面 =====
# 注意：这行代码要和 def 开头对齐（不要缩进），否则会报错
if __name__ == "__main__":
    
    # 1. 准备全新的测试数据：包含零、负数、多重重复
    test_data = [9, 0, 9, -3, 0, 9, 5]
    res_order = summarize_values(test_data)
    res_empty = summarize_values([]) # 空输入测试

    print("自定义顺序样例结果: ", res_order)
    print("自定义空输入结果: ", res_empty)

    # 2. 校验顺序和频数是否正确（按首次出现顺序：[9, 0, -3, 5]）
    assert res_order == {
        "unique": [9, 0, -3, 5],
        "counts": {9: 3, 0: 2, -3: 1, 5: 1},
        "repeated": {9, 0}
    }

    # 3. 校验传入的原列表没有被篡改
    assert test_data == [9, 0, 9, -3, 0, 9, 5]

    # 4. 校验空输入是否返回空容器
    assert res_empty == {"unique": [], "counts": {}, "repeated": set()}

    print("边界核对: PASS")
   





"""第二题"""

def apply_changes(original, updates, removals):
    """在新字典上应用修改清单；三个输入均不修改。

    original 为字符串键、整数值的字典。
    updates 为按顺序执行的 (键, 值) 元组列表，后一次更新覆盖前一次。
    所有更新完成后，再按 removals 删除；缺失键与重复删除均可忽略。
    返回 {"record": 新字典, "changed": 最终相对 original 变化的键集合}。
    改回原值、新增后又删除都不算最终变化；字典键顺序不作要求。
    每次调用产生独立结果。
    """
     # 1. 浅拷贝原字典
    record = dict(original)
    
    # 2. 依次更新
    for k, v in updates:
        record[k] = v
        
    # 3. 依次删除（用集合推导式过滤，比 for 循环 pop 更高级）
    # 把 removals 转成 set，判断查找速度更快
    removal_set = set(removals)
    record = {k: v for k, v in record.items() if k not in removal_set}
    
    # 4. 计算最终变化（利用集合的交并差运算，逻辑清晰且复杂）
    orig_keys = set(original.keys())
    rec_keys = set(record.keys())
    
    # 差集：原有新无（删除了） / 原无新有（新增了）
    deleted_keys = orig_keys - rec_keys
    added_keys = rec_keys - orig_keys
    
    # 交集：原有的也有现在的，对比值是否改变
    common_keys = orig_keys & rec_keys
    modified_keys = {k for k in common_keys if original[k] != record[k]}
    
    # 最终变化的键 = 删除 + 新增 + 修改
    changed = deleted_keys | added_keys | modified_keys
    
    return {"record": record, "changed": changed}


# ================= 样例核验=================
if __name__ == "__main__":
    
    # 自定义数据
    original = {"id": 101, "score": 85, "status": "active"}
    updates = [("score", 90), ("role", "admin"), ("score", 95), ("status", "inactive")]
    removals = ["role", "unknown_key"]
    
    # 1. 打印输入信息
    print("原记录: ", original)
    print("更新清单: ", updates)
    print("删除清单: ", removals)
    
    # 2. 调用函数
    result = apply_changes(original, updates, removals)
    
    # 3. 打印结果
    print("最终记录: ", result["record"])
    print("最终变化的键: ", result["changed"])
    
    # 4. 断言核对
    assert result == {
        "record": {"id": 101, "score": 95, "status": "inactive"},
        "changed": {"score", "status"},
    }
    assert original == {"id": 101, "score": 85, "status": "active"}
    assert updates == [("score", 90), ("role", "admin"), ("score", 95), ("status", "inactive")]
    assert removals == ["role", "unknown_key"]
    print("样例核对: PASS; 三份输入保持原样")


    # ================= 边界预测 =================
    print("\n--- 边界预测 ---")
    # 自定义边界数据：m改两次变回原样，n新增又删除
    edge_original = {"m": 100}
    edge_updates = [("m", 999), ("m", 100), ("n", 50)]
    edge_removals = ["n", "missing", "n"]
    
    edge_result = apply_changes(edge_original, edge_updates, edge_removals)
    
    print("最终记录: ", edge_result["record"])
    print("最终变化的键: ", edge_result["changed"])
    
    assert edge_result == {"record": {"m": 100}, "changed": set()}
    assert edge_original == {"m": 100}
    assert updates == [("score", 90), ("role", "admin"), ("score", 95), ("status", "inactive")] # 顺便验证上面没被串改
    assert edge_updates == [("m", 999), ("m", 100), ("n", 50)]
    assert edge_removals == ["n", "missing", "n"]
    assert apply_changes({}, [], []) == {"record": {}, "changed": set()}
    print("边界核对: PASS; 操作过，不等于最终改变")








"""第三题"""

import numpy as np
def compare_measurements(ids, baseline, current, threshold):
    """对齐两次测量；不修改输入，返回独立的新结果。

    ids 为无重复的字符串列表；baseline、current 为等长的一维整数
    NumPy 数组；值范围为 [-1000000, 1000000]；threshold 为非负整数。
    返回 {"delta": 新的一维整数数组 current - baseline,
          "alerts": abs(delta) > threshold 的编号列表，保留输入顺序,
          "normal": 其余编号到 current 值的字典}。
    恰好等于阈值属于正常；空输入也要返回三个对应的空容器。
    先把 NumPy 整数转成 Python int 再计算，避免小 dtype 溢出。
    """
       
    # 1. 转换并计算差值：使用 Numpy 向量化 astype 确保在底层直接转为 int64，防止溢出
    # 这比原答案的 for 循环 + int() 转换在底层执行效率更高
    b_arr = np.asarray(baseline, dtype=np.int64)
    c_arr = np.asarray(current, dtype=np.int64)
    
    # 直接进行矩阵减法
    delta = c_arr - b_arr
    
    # 2. 生成布尔掩码（判断哪些超阈值）
    # delta 是 np.int64，取绝对值后直接和阈值比较
    mask_alert = np.abs(delta) > threshold
    
    # 3. 使用推导式配合布尔索引，优雅地分离 alerts 和 normal
    # 取出所有满足异常条件的位置的 ids
    alerts = [ids[i] for i in range(len(ids)) if mask_alert[i]]
    
    # 取出所有满足正常条件的位置的 ids 和 current 的值（强转 int 是为了输出干净）
    normal = {ids[i]: int(c_arr[i]) for i in range(len(ids)) if not mask_alert[i]}
    
    # 返回结果字典
    return {"delta": delta, "alerts": alerts, "normal": normal}


# ================= 常规样例核验 =================
if __name__ == "__main__":
    
    # 自定义全新数据：避开 a,b,c 和 10,20,30
    ids = ["x", "y", "z", "w"]
    baseline = np.array([50, 90, -30, 100])
    current = np.array([55, 80, -30, 115])
    threshold = 8
    
    print("编号: ", ids)
    print("原测量: ", baseline)
    print("新测量: ", current)
    print("阈值: ", threshold)
    
    result = compare_measurements(ids, baseline, current, threshold)
    print("delta: ", result["delta"])
    print("alerts: ", result["alerts"])
    print("normal: ", result["normal"])
    
    # 预期算一下：delta = [5, -10, 0, 15]。绝对值超过 8 的是 -10 和 15，对应 y 和 w
    assert np.array_equal(result["delta"], np.array([5, -10, 0, 15]))
    assert result["delta"].dtype.kind in "iu"
    assert result["alerts"] == ["y", "w"]
    assert result["normal"] == {"x": 55, "z": -30}
    
    # 验证原输入未被篡改
    assert ids == ["x", "y", "z", "w"]
    assert np.array_equal(baseline, np.array([50, 90, -30, 100]))
    assert np.array_equal(current, np.array([55, 80, -30, 115]))
    print("样例核对: PASS; -10 和 15 属于异常，输入保持")
    
    
    # ================= 边界预测 =================
    print("\n--- 边界预测 ---")
    # 我们使用 int8 的极限值来测试溢出：-128 到 127
    # 如果不转为 int64 直接减，127 - (-128) 会变成 -1（溢出），转为 int64 则是 255
    edge_ids = ["p", "q", "r"]
    edge_baseline = np.array([-128, 127, 0], dtype=np.int8)
    edge_current = np.array([127, -128, 0], dtype=np.int8)
    edge_threshold = 100
    
    edge_result = compare_measurements(edge_ids, edge_baseline, edge_current, edge_threshold)
    
    print("输入 dtype: ", edge_baseline.dtype, "; 输出 dtype: ", edge_result["delta"].dtype)
    print("delta: ", edge_result["delta"])
    print("alerts: ", edge_result["alerts"])
    print("normal: ", edge_result["normal"])
    
    # 验证 int8 极值溢出被完美解决
    assert np.array_equal(edge_result["delta"], np.array([255, -255, 0]))
    assert edge_result["alerts"] == ["p", "q"]
    assert edge_result["normal"] == {"r": 0}
    
    # 空输入测试
    empty = compare_measurements([], np.array([], dtype=int), np.array([], dtype=int), 0)
    assert empty["delta"].shape == (0,) and empty["delta"].dtype.kind in "iu"
    assert empty["alerts"] == [] and empty["normal"] == {}
    
    print("空输入: ", empty)
    print("边界核对: PASS; 负数溢出被解决，空结果保持整数类型")
