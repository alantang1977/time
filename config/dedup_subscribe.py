import os
import requests
from urllib.parse import urlparse

def is_valid_url(url):
    """检查URL是否有效"""
    try:
        # 解析URL以验证基本格式
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        
        # 尝试HEAD请求检查连通性（超时设置为3秒）
        response = requests.head(url, timeout=3)
        # 接受200-399范围内的状态码
        return response.status_code < 400
    except (requests.RequestException, ValueError):
        return False

def deduplicate_subscribe():
    """对subscribe.txt文件进行去重处理"""
    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")

    # 定义输入和输出文件路径
    input_file = os.path.join(current_dir, 'config', 'subscribe.txt')
    output_dir = os.path.join(current_dir, 'config', 'deduped')
    output_file = os.path.join(output_dir, 'subscribe.txt')

    print(f"输入文件路径: {input_file}")
    print(f"输出文件路径: {output_file}")

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 '{input_file}' 不存在")
        return

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    print(f"确保输出目录存在: {output_dir}")

    # 读取文件内容并处理
    seen_urls = set()
    processed_lines = []
    invalid_urls = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            # 检查是否是HTTP/HTTPS链接
            if line.startswith(('http://', 'https://')):
                # 检查链接有效性
                if not is_valid_url(line):
                    invalid_urls.append(line)
                    print(f"无效链接: {line}")
                    continue
                # 去重处理
                if line not in seen_urls:
                    seen_urls.add(line)
                    processed_lines.append(line)
            else:
                # 非链接行直接添加
                processed_lines.append(line)

    # 写入去重后的内容到新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in processed_lines:
            f.write(line + '\n')

    print(f"处理完成!")
    print(f"写入行数: {len(processed_lines)}")
    print(f"无效链接数: {len(invalid_urls)}")
    if invalid_urls:
        print(f"无效链接列表: {invalid_urls}")
    print(f"输出文件路径: {output_file}")

if __name__ == "__main__":
    deduplicate_subscribe()    
