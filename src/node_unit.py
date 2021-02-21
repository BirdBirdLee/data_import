# 生成单位的节点csv文件
# 主键为'name'，内容为单位名

import csv
import os
import file_util

class UnitGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/node_units.csv"
    unit_header = ['name:ID', ':LABEL']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.unit_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.unit_header)
                for row in reader:
                    units_str = row['organs']  # todo ['organs']中的字段名根据实际文件修改
                    if len(units_str) < 1:
                        continue
                    # 得到unit列表
                    units = units_str.split(';')
                    unit_row = {} #待存入的一行unit的信息
                    for unit in units:
                        unit_row[':LABEL'] = 'Unit'  # 打上unit的node标签
                        # 提取出unit的名字，并作为唯一id
                        unit_row['name:ID'] = unit.strip()
                        writer.writerow(unit_row)
                        num += 1
        return num

    def generate(self):
        '''
        提取某个指定目录下的所有文件或节点
        :return:
        '''
        for one_file in os.listdir(self.input_path):
            print('开始抽取', one_file, '的节点及关系信息')
            num = self.generate_one_file(one_file)
            print('从', one_file, '中抽取了', num, '个节点或关系信息, 保存至', self.output_filename)


if __name__ == '__main__':
    g = UnitGenerator('../data_input')
    g.generate_one_file('author_info.csv')