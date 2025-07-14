import re

def extract_numbers(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # 定义正则表达式模式
        pattern = r'\+\d+\.\d+'
        
        # 查找所有匹配项
        numbers = re.findall(pattern, content)
        
        return numbers
    
    except Exception as e:
        print(f"错误: 读取文件时发生错误: {e}")
        return []

# 使用示例
file_path = r'C:\Users\yu\Desktop\evt.txt'  # 替换为你的文件路径
numbers = extract_numbers(file_path)

# 打印提取的数字
for num in numbers:
    print(num)

# 保存提取的数字到新文件
with open('extracted_numbers.txt', 'w') as f:
    f.write('\n'.join(numbers))