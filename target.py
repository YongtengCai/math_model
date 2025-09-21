#将目标文件夹中子文件夹内所有CSV文件转为宽表
import os
import pandas as pd

# 定义一个函数来递归查找所有CSV文件
def find_all_csv_files(root_dir):
    csv_files = []
    # 遍历根目录及其所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 在当前目录中查找所有CSV文件
        for filename in filenames:
            if filename.lower().endswith('.csv'):
                # 构建完整的文件路径
                full_path = os.path.join(dirpath, filename)
                csv_files.append(full_path)
    return csv_files

# 定义一个函数来处理单个CSV文件并提取数据
def process_csv_file(file_path):
    try:
        # 获取文件名（不包含扩展名）
        filename = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(filename)[0]
        
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 存储结果的字典
        result = {}
        
        # 处理文件名获取id值（从A_A格式中提取A）
        parts = file_name_without_ext.split('_')
        if len(parts) >= 2:
            base_name = parts[0]  # 使用第一部分作为id值
        else:
            base_name = file_name_without_ext  # 如果不是A_A格式，使用整个文件名
        
        # 直接获取CSV文件的第1列数据
        if not df.empty and len(df.columns) > 0:
            # 获取第1列的列名
            first_column_name = df.columns[0]
            # 提取该列的所有数据（包括标题行）作为列表
            column_data = [first_column_name]  # 添加标题行
            column_data.extend(df[first_column_name].astype(str).tolist())  # 添加数据行
            
            # 构建结果字典
            result['id'] = base_name
            result['X_time'] = column_data
            print(f"成功处理文件 {filename}，提取第1列 '{first_column_name}' 的数据，包含 {len(df[first_column_name])} 条记录")
        else:
            # 如果CSV文件为空，设置id和空的X_time
            result['id'] = base_name
            result['X_time'] = []
            print(f"警告：文件 {filename} 为空或没有列")
        
        return result
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        # 获取文件名前缀作为id，即使出错也尽量提供有意义的id
        filename = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(filename)[0]
        parts = file_name_without_ext.split('_')
        base_name = parts[0] if len(parts) >= 2 else file_name_without_ext
        
        # 返回错误情况下的结果
        return {
            'id': base_name,
            'X_time': []
        }

# 主函数：将所有CSV文件转为宽表
def csv_to_wide_table(root_dir):
    # 查找所有CSV文件
    csv_files = find_all_csv_files(root_dir)
    print(f"找到 {len(csv_files)} 个CSV文件")
    
    # 处理每个CSV文件
    processed_data = []
    for file_path in csv_files:
        data = process_csv_file(file_path)
        if data:
            processed_data.append(data)
    
    # 创建宽表
    if processed_data:
        wide_table = pd.DataFrame(processed_data)
        return wide_table
    else:
        # 如果没有处理到数据，返回空的DataFrame
        return pd.DataFrame(columns=['id', 'X_time'])

# 如果作为主程序运行
if __name__ == "__main__":
    # 获取目标文件夹路径
    target_directory = input("请输入目标文件夹路径: ")
    
    # 检查路径是否存在
    if not os.path.exists(target_directory):
        print(f"错误: 路径 '{target_directory}' 不存在")
        exit(1)
    
    # 转换CSV文件为宽表
    wide_table = csv_to_wide_table(target_directory)
    
    # 保存结果到CSV文件
    output_file = 'wide_table_result.csv'
    wide_table.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # 显示结果
    print(f"\n转换完成，宽表共有 {len(wide_table)} 行数据")
    print(f"结果已保存到: {os.path.abspath(output_file)}")
    print("\n宽表前5行:")
    print(wide_table.head())

#wide_table导出为csv文件
wide_table.to_csv('target.csv', index=False, encoding='utf-8-sig')