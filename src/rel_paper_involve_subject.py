# 生成论文-学科 这一关系
#paper_involve_subject 太长了，后面全部用 pis代替

import csv
import os
import file_util

class PISGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/rel_paper_involve_subject.csv"
    pis_header = [':START_ID',':END_ID',':TYPE']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.pis_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.pis_header)
                for row in reader:
                    subject_str = row['subject']
                    if len(subject_str) < 1:
                        continue
                    # 得到pis列表
                    piss = subject_str.split(';')
                    pis_row = {}    # 待存入的一行pis的信息
                    for pis in piss:
                        pis_row[':TYPE'] = 'paper_involve_subject'
                        # 由论文id指向subject
                        pis_row[':START_ID'] = row['uid']
                        pis_row[':END_ID'] = pis.strip()
                        writer.writerow(pis_row)
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
    g = PISGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')