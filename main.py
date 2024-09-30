import easyocr
from PIL import Image
import numpy as np
import requests
import re
import sys

def image_cut(image):
    img_cropped = []
    im = Image.open(image)
    w, h = im.size
    img_cropped.append(im.crop((w*2553/3840, h*772/2160, w*2908/3840, h*813/2160)))
    img_cropped.append(im.crop((w*2553/3840, h*946/2160, w*2908/3840, h*987/2160)))
    img_cropped.append(im.crop((w*2553/3840, h*1120/2160, w*2908/3840, h*1161/2160)))
    img_cropped.append(im.crop((w*2553/3840, h*1294/2160, w*2908/3840, h*1335/2160)))
    return img_cropped

def image_read(img_cropped):
    reader = easyocr.Reader(['ko','en'], gpu=True)
    name = []
    acc = []
    for img in img_cropped:
        temp = reader.readtext(np.array(img))
        if not temp:
            name.append(None)
            acc.append(None)
        elif temp:
            name.append(reader.readtext(np.array(img))[0][1])
            acc.append(reader.readtext(np.array(img))[0][2])
    return name, acc

def check_info(names, user_api):
    json_file = []
    for i, name in enumerate(names):
        headers = {'accept': 'application/json', 'authorization': f'bearer {user_api}',}
        response = requests.get(
            f'https://developer-lostark.game.onstove.com/armories/characters/{name}',
            headers=headers,
        )
        json_file.append(response.json())
    return json_file

def read_json(json_files):
    name, job, weapon_strong, num_gear, num_accessory, engravings, cards, gems, arkpassive = [], [], [], [], [], [], [], [], []
    for json_file in json_files:
        if json_file:
            gem_stats = [[0 for j in range(10)] for k in range(4)]  # 겁 작 멸 홍 순서
            name.append(json_file['ArmoryProfile']['CharacterName'])
            job.append(json_file['ArmoryProfile']['CharacterClassName'])
            weapon_strong_sub = json_file['ArmoryEquipment'][0]['Tooltip']
            refine_pattern = r'"Element_005": \{\s*"type": "SingleTextBox",\s*"value": "(.*?)"\s*\}'    # 상급 재련 정보를 포함한 패턴을 찾기 위한 정규 표현식
            match = re.search(refine_pattern, weapon_strong_sub, re.DOTALL) # 정규식을 사용해 상급 재련 정보를 추출
            if match:
                refine_info = match.group(1)  # 전체 상급 재련 정보
            weapon_strong.append([json_file['ArmoryEquipment'][0]['Name'].split()[0], refine_info.split('</FONT>')[-3][23:]])
            if json_file['ArmoryEngraving']['ArkPassiveEffects'] is None:
                engravings.append(None)
            elif json_file['ArmoryEngraving']['ArkPassiveEffects'][0]['Name']:
                engravings.append([[json_file['ArmoryEngraving']['ArkPassiveEffects'][0]['Name'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][0]['Grade'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][0]['Level'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][0]['AbilityStoneLevel'],
                                   ],
                                  [json_file['ArmoryEngraving']['ArkPassiveEffects'][1]['Name'],
                                   json_file['ArmoryEngraving']['ArkPassiveEffects'][1]['Grade'],
                                   json_file['ArmoryEngraving']['ArkPassiveEffects'][1]['Level'],
                                   json_file['ArmoryEngraving']['ArkPassiveEffects'][1]['AbilityStoneLevel'],
                                   ],
                                   [json_file['ArmoryEngraving']['ArkPassiveEffects'][2]['Name'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][2]['Grade'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][2]['Level'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][2]['AbilityStoneLevel'],
                                    ],
                                   [json_file['ArmoryEngraving']['ArkPassiveEffects'][3]['Name'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][3]['Grade'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][3]['Level'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][3]['AbilityStoneLevel'],
                                    ],
                                   [json_file['ArmoryEngraving']['ArkPassiveEffects'][4]['Name'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][4]['Grade'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][4]['Level'],
                                    json_file['ArmoryEngraving']['ArkPassiveEffects'][4]['AbilityStoneLevel'],
                                    ],
                                ])
            cards.append(json_file['ArmoryCard']['Effects'][0]['Items'][-1]['Name'])
            for i in range(len(json_file['ArmoryGem']['Gems'])):
                gem_name = json_file['ArmoryGem']['Gems'][i]['Name']
                if '겁화' in gem_name:
                    if '1레벨' in gem_name:
                        gem_stats[0][0] += 1
                    elif '2레벨' in gem_name:
                        gem_stats[0][1] += 1
                    elif '3레벨' in gem_name:
                        gem_stats[0][2] += 1
                    elif '4레벨' in gem_name:
                        gem_stats[0][3] += 1
                    elif '5레벨' in gem_name:
                        gem_stats[0][4] += 1
                    elif '6레벨' in gem_name:
                        gem_stats[0][5] += 1
                    elif '7레벨' in gem_name:
                        gem_stats[0][6] += 1
                    elif '8레벨' in gem_name:
                        gem_stats[0][7] += 1
                    elif '9레벨' in gem_name:
                        gem_stats[0][8] += 1
                    elif '10레벨' in gem_name:
                        gem_stats[0][9] += 1
                elif '작열' in gem_name:
                    if '1레벨' in gem_name:
                        gem_stats[1][0] += 1
                    elif '2레벨' in gem_name:
                        gem_stats[1][1] += 1
                    elif '3레벨' in gem_name:
                        gem_stats[1][2] += 1
                    elif '4레벨' in gem_name:
                        gem_stats[1][3] += 1
                    elif '5레벨' in gem_name:
                        gem_stats[1][4] += 1
                    elif '6레벨' in gem_name:
                        gem_stats[1][5] += 1
                    elif '7레벨' in gem_name:
                        gem_stats[1][6] += 1
                    elif '8레벨' in gem_name:
                        gem_stats[1][7] += 1
                    elif '9레벨' in gem_name:
                        gem_stats[1][8] += 1
                    elif '10레벨' in gem_name:
                        gem_stats[1][9] += 1
                elif '멸화' in gem_name:
                    if '1레벨' in gem_name:
                        gem_stats[2][0] += 1
                    elif '2레벨' in gem_name:
                        gem_stats[2][1] += 1
                    elif '3레벨' in gem_name:
                        gem_stats[2][2] += 1
                    elif '4레벨' in gem_name:
                        gem_stats[2][3] += 1
                    elif '5레벨' in gem_name:
                        gem_stats[2][4] += 1
                    elif '6레벨' in gem_name:
                        gem_stats[2][5] += 1
                    elif '7레벨' in gem_name:
                        gem_stats[2][6] += 1
                    elif '8레벨' in gem_name:
                        gem_stats[2][7] += 1
                    elif '9레벨' in gem_name:
                        gem_stats[2][8] += 1
                    elif '10레벨' in gem_name:
                        gem_stats[2][9] += 1
                elif '홍염' in gem_name:
                    if '1레벨' in gem_name:
                        gem_stats[3][0] += 1
                    elif '2레벨' in gem_name:
                        gem_stats[3][1] += 1
                    elif '3레벨' in gem_name:
                        gem_stats[3][2] += 1
                    elif '4레벨' in gem_name:
                        gem_stats[3][3] += 1
                    elif '5레벨' in gem_name:
                        gem_stats[3][4] += 1
                    elif '6레벨' in gem_name:
                        gem_stats[3][5] += 1
                    elif '7레벨' in gem_name:
                        gem_stats[3][6] += 1
                    elif '8레벨' in gem_name:
                        gem_stats[3][7] += 1
                    elif '9레벨' in gem_name:
                        gem_stats[3][8] += 1
                    elif '10레벨' in gem_name:
                        gem_stats[3][9] += 1
            gems.append(gem_stats)
            arkpassive.append([
                json_file['ArkPassive']['Points'][0]['Value'],
                json_file['ArkPassive']['Points'][1]['Value'],
                json_file['ArkPassive']['Points'][2]['Value'],
            ])  # 진화, 깨달음, 도약 순서
        elif not json_file:
            name.append(None)
            job.append(None)
            weapon_strong.append(None)
            engravings.append(None)
            gems.append(None)
            arkpassive.append(None)
    # profile(name, job), equipment(weapon_strong,  weapnum_gear, num_accessory), engravings(engravings), cards(card), gems(gems), arkpassive(arkpassive)
    return name, job, weapon_strong, num_gear, num_accessory, engravings, cards, gems, arkpassive

def show_info(accs, names, jobs, weapon_strongs, _num_gears, _num_accessorys, engravings, cards, gems, arkpassives):
    for i in range(4):
        if names[i] is None:
            print("인식 실패 또는 빈칸")
            print(f"=================================================")
        else:
            name = names[i]
            acc = round(float(accs[i])*100, 2)
            job = jobs[i]
            weapon_strong = weapon_strongs[i][0]
            weapon_strong_sub = weapon_strongs[i][1]
            engraving = engravings[i]
            card = cards[i]
            gem = gems[i]
            arkpassive = arkpassives[i]

            print(f"이름: {name}(인식정확도: {acc}%)")
            print(f"직업: {job}")
            print(f"무기 강화: {weapon_strong}강 (상재 +{weapon_strong_sub})")
            print(f"각인----")
            for e in range(len(engraving)):
                if engraving[e][3] is None:
                    print(f"\t{engraving[e][0]}({engraving[e][1]} {engraving[e][2]}단계)")
                elif engraving[e][3] is not None:
                    print(f"\t{engraving[e][0]}({engraving[e][1]} {engraving[e][2]}단계)(돌 {engraving[e][3]}단계)")
            print(f"카드----")
            print(f"{card}")
            print(f"보석----")
            for gem_type, row in enumerate(gem):
                for gem_level in range(len(row) -1, -1, -1):
                    gem_num = row[gem_level]
                    if gem_num != 0:
                        if gem_type == 0:
                            print(f"\t{gem_level+1}레벨 겁화 {gem_num}개")
                        elif gem_type == 1:
                            print(f"\t{gem_level+1}레벨 작열 {gem_num}개")
                        elif gem_type == 2:
                            print(f"\t{gem_level+1}레벨 멸화 {gem_num}개")
                        elif gem_type == 3:
                            print(f"\t{gem_level+1}레벨 홍염 {gem_num}개")
            print(f"앜패----")
            print(f"\t진화: {arkpassive[0]}, 깨달음: {arkpassive[1]}, 도약: {arkpassive[2]}")
            print(f"=================================================")

def start(user_api, image):
    img_cropped = image_cut(image)
    name, accs = image_read(img_cropped)
    json_file = check_info(name, user_api)
    name, job, weapon_strong, num_gear, num_accessory, engravings, cards, gems, arkpassive = read_json(json_file)
    show_info(accs, name, job, weapon_strong, num_gear, num_accessory, engravings, cards, gems, arkpassive)

# if __name__ == '__main__':
#     image = 'D:\playground\LOASpecChecker\\4.jpg'
#     user_api = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAwMTQ1NDMifQ.SUI0kkN1lfUqieqpPwmp5oE8ZPnNvyhRb0duMA97baLBXGw7WjYWZibnoP4jUwBcn8pRumNvmeWo73u-PSslrv5cPygZtIRevgRfgy-P4vALDnVKBWzn_7DZiLMOKrCWYZIMKyUwBSwKnToVoMgvFDdTQIbG3gWgmXp0B5dIrBVZZ11pSLGafzbe5lMRsFqWmL5ClkQToiQtiCNQ64GIqC9gv5p7hFQOpNv3vJ37qiowf0Co4TVRRrqas89_0RuJMjYWU04hgOjdpfdEj2mQrF6Ab3r4GwaCVCICaW2onGx8xirZSgwsctze-vGQd25i4Wf-fYgcvEUvKNCha_xxzw'
#     start(image, user_api)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # sys.argv에서 텍스트와 이미지 경로 인자를 받아서 start 함수로 전달
        user_api = sys.argv[1]
        image_path = sys.argv[2]
        start(user_api, image_path)
    else:
        print("사용법: python main.py <사용자 API 텍스트> <이미지 파일 경로>")