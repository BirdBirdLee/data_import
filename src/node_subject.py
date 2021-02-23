# 生成学科领域的节点csv文件
# 主键为'name'，内容为学科领域名字
# 学科领域从论文详情页抽取，人才详情页其实也有，暂时不抽取

import csv
import os
import file_util
import base_generator

class SubjectGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_subjects.csv"

    @property
    def header(self):
        return ['name:ID(Subject-ID)', ':LABEL']

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
                    subjects_str = row['subject']
                    if len(subjects_str) < 1:
                        continue
                    # 得到subject列表
                    subjects = subjects_str.split(';')
                    subject_row = {} #待存入的一行subject的信息
                    for subject in subjects:
                        subject_row[':LABEL'] = 'Subject'  # 打上subject的node标签
                        # 提取出subject的名字，并作为唯一id
                        subject_row['name:ID(Subject-ID)'] = subject.strip()
                        writer.writerow(subject_row)
                        num += 1
        return num


if __name__ == '__main__':
    g = SubjectGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')