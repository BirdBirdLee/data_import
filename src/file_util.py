import csv

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