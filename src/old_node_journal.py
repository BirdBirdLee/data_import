# 弃用，被 node_journal_primary_key_name 替代
# 生成论文的节点csv文件
# 主键暂定为期刊的链接，其实可以定为期刊名字，应该不重复

import csv
import os
import file_util
import base_generator

class JournalGeneratorOld(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_journals.csv"

    @property
    def header(self):
        return ['journal_id:ID', 'name', ':LABEL']


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
                    journals_str = row['magazine']
                    if len(journals_str) < 1:
                        continue
                    # 得到 期刊名-链接形式的元组
                    journal_with_link = journals_str.split('-')
                    journal_row = {} #待存入的一行期刊的信息
                    journal_row[':LABEL'] = 'Journal'  # 打上journal的node标签
                    # 提取出关键词的名字，并作为唯一id
                    journal_row['name'] = journal_with_link[0]
                    journal_row['journal_id:ID'] = 'journal-' + journal_with_link[1]
                    writer.writerow(journal_row)
                    num += 1
        return num


if __name__ == '__main__':
    g = JournalGeneratorOld('../data_input')
    g.generate_one_file('2021_journal.csv')