import glob

from modules.crypto import encode_level, decode_level
from modules.xml import xml_parse_level


def process(number, levels):
    with open(levels[number], 'r') as f:
        data = f.readlines()
        level = ''.join(data)
        level_data = xml_parse_level(level)
        object_string_full = decode_level(level_data, False).split(';')
        object_string = object_string_full[1:-1]
        map_info = object_string_full[0]

    print("\n###COL###")
    col_start = int(input("start ID: "))
    col_end = int(input("end ID: "))
    col_offset = int(input("offset: ")) - col_start

    print("\n###GROUP###")
    group_start = int(input("start ID: "))
    group_end = int(input("end ID: "))
    group_offset = int(input("offset: ")) - group_start

    obj_final = []

    str_objs = ""
    for i in object_string:
        obj = {}
        lst = i.split(',')

        # 리스트 -> 오브젝트
        for j in range(0, len(lst), 2):
            key = str(lst[j])  # Key
            value = lst[j + 1]  # Value
            obj[key] = value

        ### 그룹 ###

        # 그룹 아이디 일괄 변경
        if "57" in obj:
            groups = obj["57"].split(".")
            for k in range(0, len(groups)):
                if (
                    int(groups[k]) < 1000
                    and (int(groups[k]) >= group_start)
                    and (int(groups[k]) <= group_end)
                ):
                    groups[k] = str(int(groups[k]) + group_offset)

            obj["57"] = ".".join(groups)

        # 세컨더리 그룹 (트리거 타겟) 일괄 변경
        if "71" in obj:
            if (
                    int(obj["71"]) < 1000
                    and (int(obj["71"]) >= group_start)
                    and (int(obj["71"]) <= group_end)
            ):
                obj["71"] = str(int(obj["71"]) + group_offset)

        ### COL ###

        # Col 채널 지정 안 된 옵젝 기본값으로 (채널 1) 지정
        if obj["1"] == "899":
            if "23" not in obj:
                obj["23"] = "1"

        if "21" in obj:
            if (
                    int(obj["21"]) < 1000
                    and (int(obj["21"]) >= col_start)
                    and (int(obj["21"]) <= col_end)
            ):
                obj["21"] = str(int(obj["21"]) + col_offset)

        if "22" in obj:
            if (
                    int(obj["22"]) < 1000
                    and (int(obj["22"]) >= col_start)
                    and (int(obj["22"]) <= col_end)
            ):
                obj["22"] = str(int(obj["22"]) + col_offset)

        if "23" in obj:
            if (
                    int(obj["23"]) < 1000
                    and (int(obj["23"]) >= col_start)
                    and (int(obj["23"]) <= col_end)
            ):
                obj["23"] = str(int(obj["23"]) + col_offset)

        if "50" in obj:
            if (
                    int(obj["50"]) < 1000
                    and (int(obj["50"]) >= col_start)
                    and (int(obj["50"]) <= col_end)
            ):
                obj["50"] = str(int(obj["50"]) + col_offset)

        if "51" in obj:
            if obj["1"] == "1006":
                if "52" in obj and obj["52"] == '1':
                    if (
                        int(obj["51"]) < 1000
                        and (int(obj["51"]) >= group_start)
                        and (int(obj["51"]) <= group_end)
                    ):
                        obj["51"] = str(int(obj["51"]) + group_offset)
                else:
                    if (int(obj["51"]) < 1000
                            and (int(obj["51"]) >= col_start)
                            and (int(obj["51"]) <= col_end)
                        ):
                        obj["51"] = str(int(obj["51"]) + col_offset)

            else:
                if (
                    int(obj["51"]) < 1000
                    and (int(obj["51"]) >= group_start)
                    and (int(obj["51"]) <= group_end)
                ):
                    obj["51"] = str(int(obj["51"]) + group_offset)

        # 오브젝트 -> 리스트 -> 스트링
        temp_list = []
        keys = list(obj.keys())
        values = list(obj.values())
        for k in range(len(keys)):
            temp_list.append(keys[k])
            temp_list.append(values[k])
        str_objs += ','.join(temp_list) + ";"

    print("Saving levels...")

    gzipped_objs = encode_level(map_info + ';' + str_objs, False)
    level = level.replace(level_data, gzipped_objs)

    with open(levels[number][0:-4] + " {} {}.gmd".format(col_offset + col_start, group_offset + group_start), 'w') as ff:
        ff.write(level)


def select_level():
    levels = glob.glob('./levels/*.gmd')

    if not levels:
        print("There's no .gmd file(s) in /levels")
        exit()

    for i in range(len(levels)):
        print("{0}. {1}".format(i + 1, levels[i].split('\\')[-1]))

    number = int(input("맵을 번호로 선택해주세요: ")) - 1

    if number < 0 or number > len(levels) - 1:
        print('Incorrect input!')

    process(number, levels)


select_level()
