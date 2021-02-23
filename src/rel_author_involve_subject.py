# 生成专家-学科领域 这一关系
#author_involve_subject 太长了，后面全部用 ais代替

import csv
import os
import file_util
import base_generator

class AISGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/rel_author_involve_subject.csv"

    @property
    def header(self):
        return [':START_ID(Author-ID)',':END_ID(Subject-ID)',':TYPE']


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

                    ais_row = {}  # 待存入的一行ais的信息

                    ######################## 获得作者的主键信息 ##################
                    id = row['code']  # 获取作者的code，todo ['code']中的字段名根据实际文件修改
                    name = row['name']  # 获取作者名字，todo ['name']中的字段名根据实际文件修改
                    # 如果人的code是null，就暂时将名字作为唯一id
                    if id != 'null':
                        # 由作者id指向subject
                        ais_row[':START_ID(Author-ID)'] = 'author-' + id
                    else:
                        ais_row[':START_ID(Author-ID)'] = name
                    ####################  获得作者主键 结束######################

                    ais_row[':TYPE'] = 'author_involve_subject'

                    ################### 对于每一个 subject，生成一个作者-subject关系
                    # 获取作者subject列表，todo ['subject']中的字段名根据实际文件修改
                    subject_str = row['subject']
                    if len(subject_str) < 1:
                        continue
                    # 得到subject列表
                    subjects = subject_str.split(';')
                    for subject in subjects:
                        ais_row[':END_ID(Subject-ID)'] = subject.strip()
                        writer.writerow(ais_row)
                        num += 1
                    ############################################################
        return num

if __name__ == '__main__':
    g = AISGenerator('../data_input')
    g.generate_one_file('author_info.csv')