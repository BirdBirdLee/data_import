# 一键生成所有节点和关系

import os
import shutil

import node_author
import node_journal_primary_key_name
import node_keyword
import node_paper
import node_subject
import node_unit
import old_node_unit

import old_rel_paper_belong_to_unit
import rel_author_involve_subject
import rel_author_belong_to_unit
import rel_paper_involve_keyword
import rel_paper_involve_subject
import rel_write

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    i = 0
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
            i += 1
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    return i

def del_all_output():
    '''
    删除所有输出文件
    :return:
    '''
    del_num = del_file('../data_output')
    print('删除 ../data_output 下所有文件完成，共删除', del_num, '个文件')

if __name__ == '__main__':
    paper_path = '../data_input/paper'
    qikan_path = '../data_input/qikj'
    boshuo_path = '../data_input/boshuo'

    del_all_output()

    g = node_author.AuthorGenerator(paper_path)
    g.generate()

    g = node_journal_primary_key_name.JournalGenerator(paper_path)
    g.generate()

    g = node_keyword.KeywordGenerator(paper_path)
    g.generate()

    g = node_paper.PaperGenerator(paper_path)
    g.generate()

    g = node_subject.SubjectGenerator(paper_path)
    g.generate()

########################## 专家信息表还没爬 #####################
    # g = node_unit.UnitGenerator(paper_path)
    # g.generate()
    #
    # g = rel_author_involve_subject.AISGenerator(paper_path)
    # g.generate()
    #
    # g = rel_author_belong_to_unit.ABTUGenerator(paper_path)
    # g.generate()

####################### 专家信息表还没爬 ###########################

    g = rel_paper_involve_keyword.PIKGenerator(paper_path)
    g.generate()

    g = rel_paper_involve_subject.PISGenerator(paper_path)
    g.generate()

    g = rel_write.WriteGenerator(paper_path)
    g.generate()
