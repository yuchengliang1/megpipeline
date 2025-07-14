import re
from typing import List, Union

def find_value_in_file(file_path: str, target_value: Union[str, int, float], 
                       delimiter: str = None, column: int = None, 
                       case_sensitive: bool = True, regex: bool = False) -> List[int]:
    """
    在文件中查找指定值出现的所有行号

    参数:
        file_path: 文件路径
        target_value: 要查找的值，可以是字符串、整数或浮点数
        delimiter: 字段分隔符，None表示按整行匹配
        column: 指定列号(从0开始)，仅在delimiter不为None时有效
        case_sensitive: 是否区分大小写，仅对字符串有效
        regex: 是否使用正则表达式匹配，仅对字符串有效

    返回:
        包含匹配行号的列表(行号从1开始)
    """
    line_numbers = []
    
    # 预处理目标值
    if isinstance(target_value, str):
        if not case_sensitive:
            target_str = target_value.lower()
        else:
            target_str = target_value
    else:
        target_str = str(target_value)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.rstrip('\n')  # 去除行尾换行符
                
                if delimiter is None:
                    # 整行匹配模式
                    compare_line = line.lower() if not case_sensitive else line
                    if regex:
                        if re.search(target_str, compare_line):
                            line_numbers.append(line_number)
                    else:
                        if target_str in compare_line:
                            line_numbers.append(line_number)
                else:
                    # 列匹配模式
                    parts = line.split(delimiter)
                    if column is not None and 0 <= column < len(parts):
                        cell_value = parts[column]
                        if isinstance(target_value, str):
                            compare_value = cell_value.lower() if not case_sensitive else cell_value
                            if regex:
                                if re.search(target_str, compare_value):
                                    line_numbers.append(line_number)
                            else:
                                if target_str == compare_value:
                                    line_numbers.append(line_number)
                        else:
                            try:
                                cell_num = float(cell_value)
                                if cell_num == target_value:
                                    line_numbers.append(line_number)
                            except ValueError:
                                continue  # 单元格无法转换为数字，跳过
    
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
    except Exception as e:
        raise RuntimeError(f"读取文件时发生错误: {str(e)}")
    
    return line_numbers

# 使用示例
if __name__ == "__main__":
    # 示例1: 整行匹配
    lines = find_value_in_file(r"C:\Users\yu\Desktop\labelIndex.txt", "1")
    print(f"包含'example'的行号: {lines}")