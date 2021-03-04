import csv
import os

class AuthorCodeGenerator():

    def __init__(self, input_path: str):
        # 输入文件夹路径
        self.input_path = input_path
        # 输出文件名，追加（所有作者code存一个文件内）
        self.output_filename = "author_code.scv"
        # 输出文件目录（每个文件内的作者code单独存放）
        self.output_path = './author_output/'

    def generate_one_file_author_code(self, input_filename :str):
        '''
        提取某个文件的所有作者code
        :param input_filename:
        :return:
        '''
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            # 这里生成的作者code有两种形式，可自行选择
            # 第一种是所有作者code都记录在一个文件内，如下
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
            # 第二种是将每个文件夹对应的作者单独存放，如下
            # with open(self.output_path + 'author_' + input_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.writer(fout)
                for row in reader:
                    authors_str = row['authors']
                    if len(authors_str) < 1:
                        continue
                    # 得到 作者-code形式的元组
                    authors_with_link = authors_str.split('&')
                    author_code = ''
                    for awl in authors_with_link:
                        if len(awl) > 0:
                            # 提取名字
                            name = awl.split('-')[0]
                            # 提取作者的code,因为code是纯数字，所以加个英文开头好些，直观，又不容易重复
                            id = awl.split('-')[1]
                            # 如果人的code是null，就舍弃
                            if id != 'null':
                                writer.writerow([id])
                                num += 1
        return num

    def generate_one_dir_author_code(self):
        '''
        提取某个文件夹下的作者code
        :return:
        '''
        for one_file in os.listdir(self.input_path):
            print('开始抽取 %-30s .........' % one_file, end='')
            num = self.generate_one_file_author_code(one_file)
            print(('抽取完成，共抽取了 %-8s 个作者code, 保存至 ' + self.output_filename) % num)

if __name__ == '__main__':
    # 论文所在文件夹，如果在不同的文件夹，就运行多次
    acg = AuthorCodeGenerator('../data_input/paper')
    acg.generate_one_dir_author_code()