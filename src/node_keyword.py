# 生成关键词的节点csv文件
# 主键为'name'，即关键词名
import csv
import os
import file_util

class KeywordGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/node_keywords.csv"
    keyword_header = ['name:ID', ':LABEL']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.keyword_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.keyword_header)
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
                            keyword_row['name:ID'] = kwl.split('-')[0].strip()
                            writer.writerow(keyword_row)
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
    g = KeywordGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')