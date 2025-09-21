#将目标文件夹所有子文件夹下的所有文件.mat文件转为.csv格式
import scipy.io as sio
import pandas as pd
import numpy as np
import os
from tkinter import filedialog, Tk

# 将单个mat文件转换为csv文件
def convert_mat_to_csv(mat_file_path):
    try:
        # 读取mat文件
        mat_data = sio.loadmat(mat_file_path)
        
        # 获取MAT文件中的所有变量名（排除matlab内部变量）
        variables = [name for name in mat_data.keys() if not name.startswith('__')]
        
        if len(variables) == 0:
            print(f"警告: {mat_file_path} 中没有找到可导出的变量。")
            return False
        
        # 处理每个变量
        for var_name in variables:
            # 创建与原文件同名的csv文件路径
            mat_dir = os.path.dirname(mat_file_path)
            mat_filename = os.path.splitext(os.path.basename(mat_file_path))[0]
            csv_file_path = os.path.join(mat_dir, f"{mat_filename}_{var_name}.csv")
            
            # 获取变量数据
            data = mat_data[var_name]
            
            # 判断数据类型并导出
            if isinstance(data, np.ndarray):
                # 对于二维数组直接导出
                if len(data.shape) == 2:
                    pd.DataFrame(data).to_csv(csv_file_path, index=False, header=False)
                    print(f"已导出: {csv_file_path}")
                # 对于高维数组，先展平再导出
                else:
                    flattened_data = data.reshape(data.shape[0], -1)
                    pd.DataFrame(flattened_data).to_csv(csv_file_path, index=False, header=False)
                    print(f"已展平并导出: {csv_file_path}")
            else:
                print(f"警告: {var_name} 的数据类型 {type(data)} 不支持导出。")
                continue
        
        return True
        
    except Exception as e:
        print(f"处理 {mat_file_path} 时出错: {str(e)}")
        return False

# 批量转换目标文件夹及其子文件夹中的所有mat文件
def batch_convert_mat_to_csv():
    # 隐藏Tkinter主窗口
    root = Tk()
    root.withdraw()
    
    # 选择目标文件夹
    target_dir = filedialog.askdirectory(title="选择目标文件夹")
    
    if not target_dir:
        print("未选择文件夹，程序退出。")
        return
    
    print(f"开始处理文件夹: {target_dir}")
    print(f"正在搜索所有.mat文件，请稍候...")
    
    # 递归搜索所有.mat文件
    mat_files = []
    for root_dir, _, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith('.mat'):
                mat_files.append(os.path.join(root_dir, file))
    
    total_files = len(mat_files)
    if total_files == 0:
        print(f"在 {target_dir} 及其子文件夹中未找到.mat文件。")
        return
    
    print(f"找到 {total_files} 个.mat文件，开始转换...")
    
    # 转换每个mat文件
    success_count = 0
    for i, mat_file in enumerate(mat_files, 1):
        print(f"处理文件 {i}/{total_files}: {mat_file}")
        if convert_mat_to_csv(mat_file):  # 修复了这里，调用正确的函数
            success_count += 1
    
    print(f"转换完成！成功转换 {success_count}/{total_files} 个文件。")
    print(f"所有.csv文件已保存到原.mat文件所在位置。")

if __name__ == "__main__":
    print("批量MAT文件转CSV文件工具")
    print("=" * 50)
    print("此工具将递归处理选定文件夹及其所有子文件夹中的.mat文件")
    print("并将每个文件中的变量导出为对应的.csv文件")
    print("=" * 50)
    batch_convert_mat_to_csv()
    input("按Enter键退出...")