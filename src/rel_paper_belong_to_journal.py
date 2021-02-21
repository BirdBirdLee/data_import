# 生成论文-学科 这一关系
#paper_involve_journal 太长了，后面全部用 pbtj代替

import csv
import os
import file_util
import base_generator

class PBTJGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/rel_paper_belong_to_journal.csv"

    @property
    def header(self):
        return [':START_ID',':END_ID',':TYPE']


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


if __name__ == '__main__':
    g = PBTJGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')