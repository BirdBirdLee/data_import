# 生成论文-学科 这一关系
#paper_involve_journal 太长了，后面全部用 pbtj代替

import csv
import os
import file_util

class PBTJGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/rel_paper_belong_to_journal.csv"
    pbtj_header = [':START_ID',':END_ID',':TYPE']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.pbtj_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.pbtj_header)
                for row in reader:
                    journal_str = row['magazine']
                    if len(journal_str) < 1:
                        continue

                    journal_name = journal_str.split('-')[0].strip()
                    pbtj_row = {}    # 待存入的一行pbtj的信息
                    pbtj_row[':TYPE'] = 'paper_belong_to_journal'
                    # 由论文id指向journal
                    pbtj_row[':START_ID'] = row['uid']
                    pbtj_row[':END_ID'] = journal_name
                    writer.writerow(pbtj_row)
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
    g = PBTJGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')