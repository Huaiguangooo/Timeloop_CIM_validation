#!/bin/bash

# 执行 Python 程序
python main.py

# 检查 Python 脚本是否成功运行
if [ $? -ne 0 ]; then
    echo "Python 脚本运行失败，退出。"
    exit 1
fi

# 定义输出文件路径
output_file="./output/timeloop-mapper.stats.txt"

# 检查输出文件是否存在
if [ ! -f "$output_file" ]; then
    echo "输出文件 $output_file 不存在，退出。"
    exit 1
fi

# 提取 'Summary Stats' 行及其后内容
summary_stats=$(awk '/^Summary Stats/ {flag=1} flag' "$output_file")

# 检查是否成功提取内容
if [ -z "$summary_stats" ]; then
    echo "未找到 'Summary Stats' 行，或文件为空。"
    exit 1
fi

# 打印提取的内容
echo "$summary_stats"
