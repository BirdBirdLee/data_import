# 生成专家-学科领域 这一关系
#author_belong_to_unit 太长了，后面全部用 abtu代替

import csv
import os
import file_util

class ABTUGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/rel_author_belong_to_unit.csv"
    abtu_header = [':START_ID',':END_ID',':TYPE']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.abtu_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.abtu_header)
                for row in reader:

                    abtu_row = {}  # 待存入的一行abtu的信息

                    ######################## 获得作者的主键信息 ##################
                    id = row['code']  # 获取作者的code，todo ['code']中的字段名根据实际文件修改
                    name = row['name']  # 获取作者名字，todo ['name']中的字段名根据实际文件修改
                    # 如果人的code是null，就暂时将名字作为唯一id
                    if id != 'null':
                        # 由作者id指向unit
                        abtu_row[':START_ID'] = 'author-' + id
                    else:
                        abtu_row[':START_ID'] = name
                    ####################  获得作者主键 结束######################

                    abtu_row[':TYPE'] = 'author_belong_to_unit'

                    ################### 对于每一个 unit，生成一个作者-unit关系
                    # 获取作者unit列表，todo ['unit']中的字段名根据实际文件修改
                    unit_str = row['unit']
                    if len(unit_str) < 1:
                        continue
                    # 得到unit列表
                    units = unit_str.split(';')
                    for unit in units:
                        abtu_row[':END_ID'] = unit.strip()
                        writer.writerow(abtu_row)
                        num += 1
                        ############################################################
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
    g = ABTUGenerator('../data_input')
    g.generate_one_file('author_info.csv')