# 生成专家-学科领域 这一关系，导入的文件是成果
#author_belong_to_unit 太长了，后面全部用 abtu代替

import csv
import os
import file_util
import base_generator

class ABTUGeneratorAchievement(base_generator.BaseGenerator):

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
                    authors = row['authors']
                    for author in authors:
                        if len(author) > 1:
                            abtu_row[':START_ID(Author-ID)'] = author
                            abtu_row[':TYPE'] = 'author_belong_to_unit'

                        # 获取作者unit,生成作者-单位关系
                        unit = row['organ'].strip()
                        if len(unit) > 1:
                            abtu_row[':END_ID(Unit-ID)'] = unit
                            writer.writerow(abtu_row)
                            num += 1
                    ############################################################
        return num


if __name__ == '__main__':
    g = ABTUGeneratorAchievement('../data_input')
    g.generate_one_file('author_info.csv')