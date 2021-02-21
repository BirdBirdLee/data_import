# 生成单位的节点csv文件
# 主键为'name'，内容为单位名

import csv
import os
import file_util
import base_generator

class UnitGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_units.csv"

    @property
    def header(self):
        return ['name:ID', ':LABEL']

    def __init__(self, input_path):
        super().__init__(input_path)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.header)
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


if __name__ == '__main__':
    g = UnitGenerator('../data_input')
    g.generate_one_file('author_info.csv')