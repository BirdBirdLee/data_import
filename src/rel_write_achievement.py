# 生成写作的关系csv文件
# 暂时将不同类型的写作分开吧，成果的写作单独命名为write_achievement

import csv
import os
import file_util
import base_generator

class WriteGeneratorAchievement(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        # 暂时将不同类型的写作分开吧
        return "../data_output/rel_write_achievement.csv"

    @property
    def header(self):
        return [':START_ID(Author-ID)',':END_ID(Achievement-ID)',':TYPE']


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
                    authors_str = row['authors']
                    if len(authors_str) < 1:
                        continue
                    # 得到 作者 列表
                    authors = authors_str.split(';')
                    w_row = {}  # 待存入的一行写作关系的信息
                    w_row[':END_ID(Achievement-ID)'] = row['uid']
                    w_row[':TYPE'] = 'write_achievement'  # 写作标签
                    for author_name in authors:
                        # 提取出作者的名字，因为成果页面没有人的code，所以只能用name当id
                        w_row[':START_ID(Author-ID)'] = author_name
                        writer.writerow(w_row)
                        num += 1
        return num


if __name__ == '__main__':
    g = WriteGeneratorAchievement('../data_input')