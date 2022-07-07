import os

ROOT_DIR = 'user_agent_list'
TARGET_FILE = 'user_agents.py'

with open(TARGET_FILE, 'at') as fw:
    fw.write('ua_list = [\n')

for cur_dir_path, sub_dirs, cur_dir_files in os.walk(ROOT_DIR):
    for file in cur_dir_files:
        # 过滤蜘蛛user_agent
        if file.endswith(".txt"):
            # 两种拼接文件路径的方式效果一样
            # print(os.path.join(cur_dir_path, file))
            # print(cur_dir_path + os.sep + file)
            file_path = os.path.join(cur_dir_path, file)
            try:
                with open(file_path, 'rt') as fr:
                    with open(TARGET_FILE, 'at') as fw:
                        for line in fr.readlines():
                            fw.write("\t\'" + line.strip() + "\',\n")
            except Exception as e:
                print(e)


with open(TARGET_FILE, 'at') as fw:
    fw.write(']\n')

