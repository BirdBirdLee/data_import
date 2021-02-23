# 生成关键词的节点csv文件
# 主键为'name'，即关键词名
import csv
import os
import file_util
import base_generator

class KeywordGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_keywords.csv"

    @property
    def header(self):
        return ['name:ID(Keyword-ID)', ':LABEL']


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
                    keywords_str = row['keywords']
                    if len(keywords_str) < 1:
                        continue
                    # 得到 关键词-链接形式的元组
                    keywords_with_link = keywords_str.split(';')
                    keyword_row = {} #待存入的一行关键词的信息
                    for kwl in keywords_with_link:
                        keyword_row[':LABEL'] = 'Keyword'  # 打上keyword的node标签
                        # 提取出关键词的名字，并作为唯一id
                        if len(kwl) > 0:
                            keyword_row['name:ID(Keyword-ID)'] = kwl.split('-')[0].strip()
                            writer.writerow(keyword_row)
                            num += 1
        return num


if __name__ == '__main__':
    g = KeywordGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')