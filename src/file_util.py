import csv
import os

class FileUtil:
    '''
    文件工具类
    '''

    @classmethod
    def write_header(self, filename, header):
        '''
                不存在文件则创建文件，不存在header则写入hearder，创建header
                :return:
                '''
        # newline的作用是防止每次插入都有空行
        with open(filename, "a+", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, header)
            # 以读的方式打开csv 用csv.reader方式判断是否存在标题。
            with open(filename, "r", newline="", encoding='utf-8') as f:
                reader = csv.reader(f)
                if not [row for row in reader]:
                    writer.writeheader()
    @classmethod
    def remove_reduntant_header_one_file(self, dir_path: str, filename: str):
        '''
        删除某个文件多余的header
        :param filename:
        :return:
        '''
        num = 0
        actual_filename = dir_path + '/' + filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            # 处理好的文件换个文件夹，放在 '原文件夹名_handled' 里面
            output_filename = dir_path + '_handled/' + filename
            with open(output_filename, 'a+', encoding='utf-8', newline='') as fout:
                header = fin.readline() #读取第一行，第一行的标题要保留
                fout.write(header)
                for line in fin.readlines():
                    # 忽略以后的标题行
                    if line[0:7] != 'authors' and line[0:3] != 'DOI':
                        fout.write(line)
                        num += 1
        return num

    @classmethod
    def remove_reduntant_header_one_dir(self, dir_path: str):
        '''
        删除某个文件夹下所有文件的多余header
        :return:
        '''
        for filename in os.listdir(dir_path):
            FileUtil.remove_reduntant_header_one_file(dir_path, filename)
