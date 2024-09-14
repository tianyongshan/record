import os
import shutil

source_folder = r'D:\.NewStart\record\CMCN_文章集'
source_folder = r'./'
destination_prefix = r'D:\.NewStart\record'

keywords = ['丁东', '丛日云', '二大爷', '于建嵘', '五岳散人', '何兵', '何清涟', '余杰',
    '余英时', '信力建', '傅国涌', '冉云飞', '冯唐', '刀尔登', '刘军宁', '刘晓波',
    '刘瑜', '劳东燕', '十年砍柴', '向松祚', '吴思', '吴敬琏', '吴晓波',
    '周其仁', '周濂', '唐德刚', '大家谈', '娱乐', '孙立平', '崔卫平', '廖亦武',
    '张五常', '张千帆', '张宏杰', '张思之', '张正隆', '张辉', '张鸣', '徐友渔',
    '徐贲', '戴晴', '技术', '施卫江', '时寒冰', '易中天',
    '朱大可', '朱学勤', '李慎之', '李承鹏', '李银河', '杨小凯', '杨继绳', '林达',
    '柏杨', '柏杨曰', '梁文道', '武志红', '殷海光', '江平', '沈志华', '熊培云',
    '王元化', '王学泰', '王小波', '王跃文', '瘦竹', '百家争鸣',
    '秦晖', '程晓农', '章诒和', '童大焕', '笑蜀', '罗翔', '羽戈', '胡星斗', '胡适',
    '范立群', '茅于轼', '茅海建', '萧功秦', '萧瀚', '葛兆光', '葛剑雄', '袁伟时',
    '袁腾飞', '许倬云', '许志永', '许知远', '许章润', '许纪霖', '费孝通', '贺卫方',
    '资中筠', '邵燕祥', '郎咸平', '郑也夫', '郑永年', '郭于华', '野夫', '金雁',
    '钱理群', '钱穆', '阎连科', '阿城', '陈丹青', '陈乐民', '陈志武', '雷颐',
    '韦大林', '韩寒', '顾准', '顾诚', '马勇', '高华', '高王凌', '鲍鹏山', '黄万里',
    '黄仁宇', '黄泰', '黄鹤升', '齐邦媛', '龙应台','张维迎','冯骥才'
]

for keyword in keywords:
    destination_folder = os.path.join(destination_prefix, keyword)
    os.makedirs(destination_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    if filename.lower().endswith('.md'):
        # print(f"Processing file: {filename}")
        for keyword in keywords:
            if keyword in filename:
                print(f"Keyword '{keyword}' found in filename")
                destination_folder = os.path.join(destination_prefix, keyword)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                source_file = os.path.join(source_folder, filename)
                destination_file = os.path.join(destination_folder, filename)
                try:
                    shutil.move(source_file, destination_file)
                    print(f"Moved {filename} to {destination_folder}")
                except Exception as e:
                    print(f"Error moving {filename}: {str(e)}")
                break
        # else:
            # print(f"No keyword found for file: {filename}")

print("File moving completed.")
