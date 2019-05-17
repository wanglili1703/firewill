# coding: utf-8
import base64
import datetime
import hashlib
import hmac
import json
import os
import random
import string

import pyDes
import xlwt

from code_gen.lib.district_code import DistrictCode

class Utility:
    def __init__(self):
        pass

    class GetOsPath(object):
        def get_current_path(self):

            current_path = os.getcwd()
            return current_path

        def get_father_path(self):

            current_path = os.getcwd()
            father_path = os.path.dirname(current_path)
            return father_path

    class GetData(object):
        # 随机生成手机号码
        def mobile(self):
            prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                       "153", "155", "156", "157", "158", "159", "186", "187", "188", "160", "170", "171"]

            mobile = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

            return mobile

        # 随机生成字母数字
        def GenAlphanumeric(self, length):
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

        # 随机生成姓名
        def chinese_name(self):
            last_name = [u'赵', u'钱', u'孙', u'李', u'周', u'吴', u'郑', u'王', u'冯', u'陈', u'褚', u'卫',
                         u'蒋', u'沈', u'韩', u'杨', u'朱', u'秦', u'尤', u'许', u'何', u'吕', u'施', u'张',
                         u'孔', u'曹', u'严', u'华', u'金', u'魏', u'陶', u'姜', u'戚', u'谢', u'邹', u'喻',
                         u'柏', u'水', u'窦', u'章', u'云', u'苏', u'潘', u'葛', u'奚', u'范', u'彭', u'郎',
                         u'鲁', u'韦', u'昌', u'马', u'苗', u'凤', u'花', u'方', u'俞', u'任', u'袁', u'柳',
                         u'酆', u'鲍', u'史', u'唐', u'费', u'廉', u'岑', u'薛', u'雷', u'贺', u'倪', u'汤',
                         u'滕', u'殷', u'罗', u'毕', u'郝', u'邬', u'安', u'常', u'乐', u'于', u'时', u'傅',
                         ]
            first_name_1 = [u'皮', u'卞', u'齐', u'康', u'伍', u'余', u'元', u'卜', u'顾', u'孟', u'平', u'黄',
                            u'和', u'穆', u'萧', u'尹', u'姚', u'邵', u'湛', u'汪', u'祁', u'毛', u'禹', u'狄',
                            u'甄', u'麴', u'家', u'封', u'芮', u'羿', u'储', u'靳', u'汲', u'邴', u'糜', u'松',
                            u'熊', u'纪', u'舒', u'屈', u'项', u'祝', u'董', u'梁', u'杜', u'阮', u'蓝', u'闵',
                            u'席', u'季', u'麻', u'强', u'贾', u'路', u'娄', u'危', u'江', u'童', u'颜', u'郭',
                            u'梅', u'盛', u'林', u'刁', u'锺', u'徐', u'邱', u'骆', u'高', u'夏', u'蔡', u'田',
                            u'樊', u'胡', u'凌', u'霍', u'虞', u'万', u'支', u'柯', u'昝', u'管', u'卢', u'莫',
                            ]
            first_name_2 = [u'经', u'房', u'裘', u'缪', u'干', u'解', u'应', u'宗', u'丁', u'宣', u'贲', u'邓',
                            u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'',
                            u'郁', u'单', u'杭', u'洪', u'包', u'诸', u'左', u'石', u'崔', u'吉', u'钮', u'龚',
                            u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'',
                            u'程', u'嵇', u'邢', u'滑', u'裴', u'陆', u'荣', u'翁', u'荀', u'羊', u'於', u'惠',
                            u'米', u'贝', u'明', u'臧', u'计', u'伏', u'成', u'戴', u'谈', u'宋', u'茅', u'庞',
                            u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'',
                            ]

            name = random.choice(last_name) + random.choice(first_name_1) + random.choice(first_name_2)

            return name

        def english_name(self):
            last_name = ['Aaron', 'Abbott', 'Abel', 'Abner', 'Abraham', 'Adair', 'Adam', 'Addison', 'Adolph', 'Adonis',
                         'Adrian', 'Ahern', 'Smith', 'Jones', 'Williams', 'Taylor', 'Brown', 'Davies', 'Evans',
                         'Wilson', 'Thomas', 'Johnson', 'Roberts', 'Robinson',
                         ]

            name = random.choice(last_name)

            return name

        def salary(self):
            integer = random.randint(8000, 12000)
            decimal = random.randint(0, 99)
            num = str(integer) + '.' + str(decimal)
            return num

        # card_type=0借记卡,card_type=1信用卡
        def bank_card_no(self, card_bin=None, card_type=0):
            # 招商银行借记卡16位,交通银行借记卡17位,其他借记卡19位
            debit_card = {
                '456351': [u'中国银行借记卡', 11],
                '103000': [u'农业银行借记卡', 11],
                '415599': [u'民生银行借记卡', 11],
                '622202': [u'工商银行借记卡', 13],
                '421437': [u'中信银行借记卡', 11],
                '623595': [u'南粤银行借记卡', 13],
                '620522': [u'上海银行储蓄卡', 12],
            }

            credit_card = {
                '625976': [u'光大银行信用卡', 10],
                '622228': [u'浦发银行信用卡', 10],
                '625961': [u'兴业银行信用卡', 10],
                '6259'
                '65': [u'建设银行信用卡', 10],
                '53098': [u'工商银行信用卡', 11],
                '404117': [u'农业银行信用卡', 10],
                '403391': [u'中信银行信用卡', 10],
                '622761': [u'中国银行信用卡', 10],
                '439225': [u'招商银行信用卡', 10],
                '356829': [u'上海银行信用卡', 10],
            }

            card_tail_no = ''

            chars = '1234567890'
            length = len(chars) - 1

            if card_bin is None:
                if card_type == 0:
                    card_bin = random.choice(list(debit_card.keys()))
                else:
                    card_bin = random.choice(list(credit_card.keys()))
            else:
                card_bin = card_bin

            card_tail_digit = debit_card[card_bin][1] if card_type == 0 else credit_card[card_bin][1]

            for i in range(card_tail_digit):
                card_tail_no += chars[random.randint(0, length)]

            bank_card_no = card_bin + card_tail_no + '-' + debit_card[card_bin][
                0] if card_type == 0 else card_bin + card_tail_no + '-' + credit_card[card_bin][0]

            return bank_card_no

        def district_code(self):
            state = None
            city = None

            data = DistrictCode.CODES
            district_list = data.split('\n')
            code_list = []

            for node in district_list:
                if node[10:11] != ' ':
                    state = node[10:].strip()
                if node[10:11] == ' ' and node[12:13] != ' ':
                    city = node[12:].strip()
                if node[10:11] == ' ' and node[12:13] == ' ':
                    district = node[14:].strip()
                    code = node[0:6]
                    code_list.append(
                        {"state": state, "city": city, "district": district,
                         "code": code})

            return code_list

        def id_no(self):
            # 生成身份证号
            code_list = self.district_code()
            id_card = code_list[random.randint(0, len(code_list) - 1)]['code']
            id_card += str(random.randint(1930, 1992))
            da = datetime.date.today() + datetime.timedelta(days=random.randint(1, 366))
            id_card += da.strftime('%m%d')
            id_card += str(random.randint(100, 999))

            count = 0
            weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            for i in range(0, 17):
                count += int(id_card[i]) * weight[i]
            id_card += '10X98765432'[count % 11]
            return id_card

    class ExcelHandle(object):
        def __init__(self):
            self._data = Utility.GetData()

        def write_to_excel(self, excel_path, rows):
            workbook = xlwt.Workbook()
            return workbook

    class StringHandle(object):
        def json_python(self, data):
            data_json = json.dumps(data, indent=2)
            data_python = json.loads(data_json)

            if type(data_python) is unicode:
                d = eval(data_python)
                return d

            return data_python

        def replace_in_turn(self, string, str_attrs):
            if string.count('%s') == str_attrs.__len__():
                string = string % tuple(str_attrs)
            else:
                raise Exception('be sure replace count is same !!!')
            return string

    class EncryptHandle(object):
        def des3_encrypt(self, key, ivect, text):
            cipher = pyDes.triple_des(key[0:24], mode=pyDes.CBC, IV=ivect, padmode=pyDes.PAD_PKCS5)
            r = cipher.encrypt(text)
            return base64.standard_b64encode(r)

        def encrypt_password(self, password_clear, current_device_id):  # huaxin_xjb密码加密规则
            key = current_device_id + '00'
            ivect = 'sh-hx-zq'
            password = self.des3_encrypt(str(key), ivect, password_clear)

            return password

        def create_signature(self, request_params, current_device_id):
            key = current_device_id + 'shhxzq'
            msg = request_params.encode('utf-8')
            signature = hmac.new(key=key, msg=msg, digestmod=hashlib.sha1).hexdigest()
            return signature.upper()

    class DateUtil:

        # 返回年月日
        def getToday(self):
            today = datetime.date.today()
            return today


if __name__ == '__main__':
    m = Utility
    print Utility.GetData().GenAlphanumeric(16)
    # print m.EncryptHandle().des3_encrypt_1(key='aab3238922bcc25a6f606eb525ffdc5600', iv='sh-hx-zq', data='135790')
