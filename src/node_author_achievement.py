# 生成专家的节点csv文件
# 主键是 'author_id',内容为'author-' + 知网的 'code'，例如 'author-12345678'

import csv
import os
import file_util
import base_generator

class AuthorGeneratorFromAchievement(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_authors.csv"

    @property
    def header(self):
        return ['author_id:ID(Author-ID)', 'name', ':LABEL']


    def __init__(self, input_path):
        super().__init__(input_path)

    def generate_one_file(self, input_filename):
        num = 0 #生成的节点或关系数
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
                    author_row = {}  # 待存入的一行作者的信息
                    for author_name in authors:
                        author_row[':LABEL'] = 'Author'  # 打上author的node标签
                        # 提取出作者的名字，因为成果页面没有人的code，所以只能用name当id
                        author_row['author_id:ID(Author-ID)'] = author_name
                        writer.writerow(author_row)
                        num += 1
        return num

if __name__ == '__main__':
    g = AuthorGeneratorFromAchievement('../data_input/achievement')