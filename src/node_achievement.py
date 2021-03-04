# 生成成果的节点csv文件
# 主键为'achievement_id'，内容为生成的uuid

import csv
import os
import file_util
import base_generator

class AchievementGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/node_achievements.csv"

    @property
    def header(self):

        return ['achievement_id:ID(Achievement-ID)','book_code', 'category',
                'evaluate', 'in_time', 'keywords', 'level','organ', 'pass_time',
                'subject_code', 'summary', 'title', 'type','uid', 'url', 'year', ':LABEL']


    def __init__(self, input_path):
        super().__init__(input_path)


    def generate_one_file(self, input_filename):
        '''
        提取出某个文件内的所有关于成果节点的信息
        :param input_filename:
        :return:
        '''
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.header)
                achievement_row = {}  # 一行成果节点的信息，期刊和博硕整合在一起，用type属性区分
                achievement_row[':LABEL'] = 'Achievement'
                for row in reader:

                    # 抽取属性，其中作者，关键词，期刊，学科领域这几个字段直接通过关系链接
                    # unit 因为还没写关于单位的代码，所以暂时在节点中保留这一属性
                    achievement_row['achievement_id:ID(Achievement-ID)'] = row['uid']
                    achievement_row['book_code'] = row['book_code']
                    # achievement_row['authors'] = row['authors']
                    achievement_row['category'] = row['category']
                    achievement_row['evaluate'] = row['evaluate']
                    # achievement_row['keywords'] = row['keywords']
                    achievement_row['in_time'] = row['in_time']
                    achievement_row['pass_time'] = row['pass_time']
                    achievement_row['level'] = row['level']
                    achievement_row['summary'] = row['summary']
                    # 注意这里的subject_code是数字，和之前论文的学科领域不一样
                    achievement_row['subject_code'] = row['subject_code']
                    # 成果的单位直接用成果界面的单位，而且只有一个单位
                    # todo 单位修改成关系形式
                    achievement_row['unit'] = row['organ']
                    achievement_row['title'] = row['title']
                    achievement_row['type'] = row['type']
                    # achievement_row['mentor'] = row['mentor']
                    achievement_row['url'] = row['url']
                    achievement_row['year'] = row['year']

                    writer.writerow(achievement_row)
                    num += 1
        return num


if __name__ == '__main__':
    g = AchievementGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')