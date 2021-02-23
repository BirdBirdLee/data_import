# 生成论文的节点csv文件
# 主键为'paper_id'，内容为生成的uuid
# 此版本直接将原始论文字段的所有数据原封不动存到图数据库中了，后面会有个新的处理后的版本

import csv
import os
import file_util
import base_generator

class PaperGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_papers.csv"

    @property
    def header(self):
        # return ['paper_id:ID', 'DOI','authors','cate_code','db','keywords'
        # ,'journal','unit','special','subject','summary','title', ':LABEL'
        # ,'type', 'mentor', 'url', 'year']

        return ['paper_id:ID(Paper-ID)', 'DOI', 'cate_code', 'db', 'units',
                'special', 'summary', 'title', ':LABEL'
                , 'type', 'url', 'year']


    def __init__(self, input_path):
        super().__init__(input_path)


    def generate_one_file(self, input_filename):
        '''
        提取出某个文件内的所有关于论文节点的信息
        :param input_filename:
        :return:
        '''
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.header)
                paper_row = {}  # 一行论文节点的信息，期刊和博硕整合在一起，用type属性区分
                paper_row[':LABEL'] = 'Paper'
                for row in reader:

                    # 抽取属性，其中作者，关键词，期刊，学科领域这几个字段直接通过关系链接
                    # unit 因为还没写关于单位的代码，所以暂时在节点中保留这一属性
                    # mentor即导师属性暂时删除
                    paper_row['paper_id:ID(Paper-ID)'] = row['uid']
                    paper_row['DOI'] = row['DOI']
                    # paper_row['authors'] = row['authors']
                    paper_row['cate_code'] = row['cate_code']
                    paper_row['db'] = row['db']
                    # paper_row['keywords'] = row['keywords']
                    # paper_row['journal'] = row['journal']
                    paper_row['units'] = row['organs']
                    paper_row['special'] = row['special']
                    # paper_row['subject'] = row['subject']
                    # 注意概要中可能包含换行,但csv不能多行
                    paper_row['summary'] = row['summary'].replace('\n', ' ').replace('\r', '')
                    paper_row['title'] = row['title']
                    paper_row['type'] = row['type']
                    # paper_row['mentor'] = row['mentor']
                    paper_row['url'] = row['url']
                    paper_row['year'] = row['year']

                    writer.writerow(paper_row)
                    num += 1
        return num


if __name__ == '__main__':
    g = PaperGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')