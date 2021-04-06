# 生成专家-单位 这一关系，输入的是专家详细信息文件
#author_belong_to_unit 太长了，后面全部用 abtu代替

import csv
import os
import file_util
import base_generator

class ABTUGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/rel_author_belong_to_unit.csv"

    @property
    def header(self):
        return [':START_ID(Author-ID)',':END_ID(Unit-ID)',':TYPE']


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

                    abtu_row = {}  # 待存入的一行abtu的信息

                    ######################## 获得作者的主键信息 ##################
                    id = row['code']  # 获取作者的code
                    name = row['name']  # 获取作者名字
                    # 如果人的code是null，就暂时将名字作为唯一id
                    if id != 'null':
                        # 由作者id指向unit
                        abtu_row[':START_ID(Author-ID)'] = 'author-' + id
                    else:
                        abtu_row[':START_ID(Author-ID)'] = name
                    ####################  获得作者主键 结束######################

                    abtu_row[':TYPE'] = 'author_belong_to_unit'

                    ################### 对于每一个 unit，生成一个作者-unit关系
                    # 获取作者unit列表
                    unit_str = row['school']
                    if len(unit_str) < 1:
                        continue
                    # 得到unit列表
                    units = unit_str.split(';')
                    for unit in units:
                        abtu_row[':END_ID(Unit-ID)'] = unit.strip()
                        writer.writerow(abtu_row)
                        num += 1
                        ############################################################
        return num


if __name__ == '__main__':
    g = ABTUGenerator('../data_input')
    g.generate_one_file('author_info.csv')