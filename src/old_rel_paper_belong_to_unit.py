# 生成论文-单位 这一关系
#paper_belong_to_unit 太长了，后面全部用 pbtu代替
# 此代码为旧方式，使用的是论文下面的单位，已弃用，以后使用人才详情页的单位信息


import csv
import os
import file_util

class PBTUGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/rel_paper_belong_to_unit.csv"
    pbtu_header = [':START_ID',':END_ID',':TYPE']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.pbtu_header)

    def generate_one_file(self, input_filename):
        num = 0  # 生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.pbtu_header)
                for row in reader:
                    unit_str = row['organs']
                    if len(unit_str) < 1:
                        continue
                    # 得到pbtu列表
                    pbtus = unit_str.split(';')
                    pbtu_row = {}    # 待存入的一行pbtu的信息
                    for pbtu in pbtus:
                        pbtu_row[':TYPE'] = 'paper_belong_to_unit'
                        # 由论文id指向unit
                        pbtu_row[':START_ID'] = row['uid']
                        pbtu_row[':END_ID'] = pbtu.strip()
                        writer.writerow(pbtu_row)
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
    g = PBTUGenerator('../data_input')
    g.generate_one_file('2021_journal.csv')