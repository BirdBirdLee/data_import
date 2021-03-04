# 生成写作的关系csv文件

import csv
import os
import file_util
import base_generator
import logging

class WriteGenerator(base_generator.BaseGenerator):

    @property
    def output_filename(self):
        return "../data_output/rel_write.csv"

    @property
    def header(self):
        return [':START_ID(Author-ID)',':END_ID(Paper-ID)',':TYPE']


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
                    authors_str = row['authors']
                    if len(authors_str) < 1:
                        continue
                    # 得到 作者-code形式的元组
                    authors_with_link = authors_str.split('&')
                    write_dict = {}  # 待存入的一行write关系的信息
                    for awl in authors_with_link:
                        write_dict[':TYPE'] = 'write'  # 打上write的rel标签
                        write_dict[':END_ID(Paper-ID)'] = row['uid']   #write关系的结束节点是论文
                        # 提取出作者的名字、code，把code作为唯一id，利用知网帮忙去重
                        # todo 这里有个问题，有的人code是null，所以如果链接是null
                        if len(awl) > 0:
                            # 提取名字
                            name = awl.split('-')[0]
                            # 提取作者的code,因为code是纯数字，所以加个英文开头好些，直观，又不容易重复
                            try:
                                id = awl.split('-')[1]
                                # 如果人的code是null，就暂时将名字作为唯一id
                                if id != 'null':
                                    write_dict[':START_ID(Author-ID)'] = 'author-' + id
                                else:
                                    write_dict[':START_ID(Author-ID)'] = name
                                writer.writerow(write_dict)
                                num += 1
                            except IndexError:
                                logging.debug('提取作者id时出现错误，authors字段如下:', end=' ')
                                logging.debug(awl)
        return num


if __name__ == '__main__':
    g = WriteGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')