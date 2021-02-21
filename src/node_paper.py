# 生成论文的节点csv文件
# 主键为'paper_id'，内容为生成的uuid
# 此版本直接将原始论文字段的所有数据原封不动存到图数据库中了，后面会有个新的处理后的版本

import csv
import os
import file_util

class PaperGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/node_papers.csv"
    paper_header = ['paper_id:ID', 'DOI','authors','cate_code','db','keywords'
        ,'magazine','organs','special','subject','summary','title', ':LABEL'
        ,'type', 'mentor', 'url', 'year']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.paper_header)

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
                writer = csv.DictWriter(fout, self.paper_header)
                for row in reader:
                    # 因为csv文件设置的header是'paper_id:ID',原始文件是'uid'，这里要改一下键的名字
                    row['paper_id:ID'] = row['uid']
                    row.pop('uid')
                    row[':LABEL'] = 'Paper'    #打上paper的node标签
                    writer.writerow(row)
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
    g = PaperGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')