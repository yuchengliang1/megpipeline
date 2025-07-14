def filter_file_by_line_numbers(input_file: str, output_file: str, line_numbers: list[int]) -> None:
    """
    根据行号列表筛选文件内容并保存到新文件
    
    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
        line_numbers: 要保留的行号列表(行号从1开始)
    """
    # 将行号转换为集合以加速查找
    line_set = set(line_numbers)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            # 逐行处理输入文件
            for line_number, line in enumerate(infile, 1):
                if line_number in line_set:
                    outfile.write(line)
    
    except FileNotFoundError:
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    except Exception as e:
        raise RuntimeError(f"处理文件时发生错误: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 示例行号数组
    line_numbers = [1, 7, 10, 15, 19, 22, 28, 31, 36, 38, 42, 48, 50, 56, 58, 62, 65, 70]
    
    # 输入和输出文件路径
    input_file = r"C:\Users\yu\Desktop\extracted_numbers.txt"
    output_file = r"C:\Users\yu\Desktop\label1.txt"

    # 执行筛选
    filter_file_by_line_numbers(input_file, output_file, line_numbers)
    
    print(f"已根据行号筛选文件并保存到 {output_file}")