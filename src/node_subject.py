# 生成学科领域的节点csv文件
# 主键为'name'，内容为学科领域名字
# 学科领域从论文详情页抽取，人才详情页其实也有，暂时不抽取

import csv
import os
import file_util

class SubjectGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/node_subjects.csv"
    subject_header = ['name:ID', ':LABEL']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.subject_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.subject_header)
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
                        subject_row['name:ID'] = subject.strip()
                        writer.writerow(subject_row)
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
    g = SubjectGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')