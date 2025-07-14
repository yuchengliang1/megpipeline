def check_value_range(file_path, min_diff, max_diff):
    try:
        with open(file_path, 'r') as f:
            # 读取文件并转换为浮点数列表
            numbers = [float(line.strip()) for line in f]
        
        # 计算相邻元素的差值
        diffs = [b - a for a, b in zip(numbers[:-1], numbers[1:])]
        
        # 检测每个差值是否在范围内
        for i, diff in enumerate(diffs):
            if not (min_diff <= diff <= max_diff):
                print(f"错误：索引 {i} 和 {i+1} 之间的差值为 {diff}，超出范围 [{min_diff}, {max_diff}]")
        return False
        
        print("所有相邻数字的差值都在指定范围内。")
        return True
    
    except ValueError as e:
        print(f"错误：文件包含无法转换为数字的行: {e}")
        return False
    except Exception as e:
        print(f"错误：发生未知错误: {e}")
        return False

# 使用示例
file_path = r'C:\Users\yu\extracted_numbers.txt'  # 替换为你的文件路径
min_diff = -14.0  # 最小差值
max_diff = 14.0   # 最大差值

check_value_range(file_path, min_diff, max_diff)