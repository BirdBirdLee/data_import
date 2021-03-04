# 一键生成所有节点和关系

import os
import shutil

import file_util

import node_achievement
import node_author
import node_author_achievement
import node_journal_primary_key_name
import node_keyword
import node_keyword_achievement
import node_paper
import node_subject
import node_unit
import node_unit_achievement
import old_node_unit

import old_rel_paper_belong_to_unit
import rel_achievement_involve_keyword
import rel_author_involve_subject
import rel_author_belong_to_unit
import rel_author_belong_to_unit_achievement
import rel_paper_belong_to_journal
import rel_paper_involve_keyword
import rel_paper_involve_subject
import rel_write
import rel_write_achievement

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
    # paper_path = '../data_input/paper'
    paper_path = '../data_input/paper_handled'
    # achievement_path = '../data_input/achievement'
    achievement_path = '../data_input/achievement_handled'
    # 为了减少工作量，把期刊内的和博硕的论文统一为 论文 了，papart_path 内的文件包含这两者
    # qikan_path = '../data_input/qikj'
    # boshuo_path = '../data_input/boshuo'

    # 删除所有输出文件
    del_all_output()

    # 删除所有handled文件夹下的文件
    del_file('../data_input/paper_handled')
    del_file('../data_input/achievement_handled')

    # 删除成果文件多余的标题行
    file_util.FileUtil.remove_reduntant_header_one_dir('../data_input/achievement')

    # 删除论文文件多余的标题行
    file_util.FileUtil.remove_reduntant_header_one_dir('../data_input/paper')


    ###################################### 期刊、博硕 的信息抽取开始##############################
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

                      ########### 专家信息表还没爬 ########
    # g = node_unit.UnitGenerator(paper_path)
    # g.generate()
    #
    # g = rel_author_involve_subject.AISGenerator(paper_path)
    # g.generate()
    #
    # g = rel_author_belong_to_unit.ABTUGenerator(paper_path)
    # g.generate()

                   ######### 专家信息表还没爬 ###########

    g = rel_paper_belong_to_journal.PBTJGenerator(paper_path)
    g.generate()

    g = rel_paper_involve_keyword.PIKGenerator(paper_path)
    g.generate()

    g = rel_paper_involve_subject.PISGenerator(paper_path)
    g.generate()

    g = rel_write.WriteGenerator(paper_path)
    g.generate()


    ############################期刊、博硕 信息抽取结束##################################




    ####################################成果信息抽取开始#######################################

    # g = node_achievement.AchievementGenerator(achievement_path)
    # g.generate()
    #
    # g = node_author_achievement.AuthorGeneratorFromAchievement(achievement_path)
    # g.generate()
    #
    # g = node_keyword_achievement.KeywordGeneratorAchievement(achievement_path)
    # g.generate()
    #
    # g = rel_write_achievement.WriteGeneratorAchievement(achievement_path)
    # g.generate()
    #
    # g = node_unit_achievement.UnitGeneratorAchievement(achievement_path)
    # g.generate()
    #
    # g = rel_author_belong_to_unit_achievement.ABTUGeneratorAchievement(achievement_path)
    # g.generate()



    #################################成果信息抽取结束##########################################
