# 所有生成类的基类，为了后面的代码好写

import csv
import os
import abc
import file_util
import logging


class BaseGenerator:

    def __init__(self, input_path):
        # print('基础类创建')
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.header)

    # 相当于抽象数据类型，是建库文件的输出文件名
    @property
    @abc.abstractmethod
    def output_filename(self):
        pass

    # 相当于抽象数据类型，是建库文件的header
    @property
    @abc.abstractmethod
    def header(self):
        pass

    @abc.abstractmethod
    def generate_one_file(self, input_filename):
        pass

    @abc.abstractmethod
    def generate(self):
        '''
        提取某个指定目录下的所有文件或节点
        :return:
        '''
        for one_file in os.listdir(self.input_path):
            print('开始抽取 %-30s .........' % one_file, end='')
            num = self.generate_one_file(one_file)
            print(('抽取完成，共抽取了 %-8s 个节点或关系信息, 保存至 ' + self.output_filename) % num)