import pandas as pd
import unicodedata
import regex as re
from pyvi import ViTokenizer

bang_nguyen_am = [
    ["a", "à", "á", "ả", "ã", "ạ", "a"],
    ["ă", "ằ", "ắ", "ẳ", "ẵ", "ặ", "aw"],
    ["â", "ầ", "ấ", "ẩ", "ẫ", "ậ", "aa"],
    ["e", "è", "é", "ẻ", "ẽ", "ẹ", "e"],
    ["ê", "ề", "ế", "ể", "ễ", "ệ", "ee"],
    ["i", "ì", "í", "ỉ", "ĩ", "ị", "i"],
    ["o", "ò", "ó", "ỏ", "õ", "ọ", "o"],
    ["ô", "ồ", "ố", "ổ", "ỗ", "ộ", "oo"],
    ["ơ", "ờ", "ớ", "ở", "ỡ", "ợ", "ow"],
    ["u", "ù", "ú", "ủ", "ũ", "ụ", "u"],
    ["ư", "ừ", "ứ", "ử", "ữ", "ự", "uw"],
    ["y", "ỳ", "ý", "ỷ", "ỹ", "ỵ", "y"],
]
bang_ky_tu_dau = ["", "f", "s", "r", "x", "j"]


def chuan_hoa_unicode(text):
    text = unicodedata.normalize("NFC", text)
    return text


nguyen_am_to_ids = {}
for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)


def is_valid_vietnam_word(word):
    chars = word.split()
    nguyen_am_index = -1
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x != -1:
            if nguyen_am_index == -1:
                nguyen_am_index = index
            else:
                if index - nguyen_am_index != 1:
                    return False
                nguyen_am_index = index
    return True


def chuan_hoa_dau_tu_tieng_viet(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = word.split()
    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False

    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == "q":
                chars[index] = "u"
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == "g":
                chars[index] = "i"
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            nguyen_am_index.append(index)
    if len(nguyen_am_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = nguyen_am_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = (
                        bang_nguyen_am[5][dau_cau]
                        if chars[1] == "i"
                        else bang_nguyen_am[9][dau_cau]
                    )
            return "".join(chars)
        return word

    for index in nguyen_am_index:
        x, y = nguyen_am_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            return "".join(chars)

    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
        else:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    return "".join(chars)


def chuan_hoa_dau_cau_tieng_viet(sentence):
    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(
            r"(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)", r"\1/\2/\3", word
        ).split("/")
        # print(cw)
        if len(cw) == 3:
            cw[1] = chuan_hoa_dau_tu_tieng_viet(cw[1])
        words[index] = "".join(cw)
    return " ".join(words)


def tach_tu_tieng_viet(text):
    text = ViTokenizer.tokenize(text)
    return text


def chuyen_chu_thuong(text):
    return text.lower()


def chuan_hoa_cau(text):
    text = re.sub(
        r"[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_.]",
        " ",
        text,
    )  # giữ những regex đã đề cập
    text = re.sub(r"\s+", " ", text).strip()
    return text


with open("stopword.txt", "r", encoding="utf-8") as f:
    stopwords_list = f.read().split("\n")


def bo_stopword(text):
    # stopwords_list = open('stopword.txt', 'r').read().split('\n')
    text = text.split()
    non_sw_text = []
    for word in text:
        if word not in stopwords_list:
            non_sw_text.append(word)
    result = " ".join([str(item) for item in non_sw_text])
    return result
    # return


def tien_xu_li(text):
    text = chuan_hoa_unicode(text)
    print("1- chuan hoa unicode \n" + text)
    text = chuan_hoa_dau_cau_tieng_viet(text)
    print("2- chuan hoa dau cau tieng viet \n" + text)
    text = tach_tu_tieng_viet(text)
    print("3- tach tu tieng viet \n" + text)
    text = chuyen_chu_thuong(text)
    print("4- chuyen chu thuong \n" + text)
    text = chuan_hoa_cau_2(text)
    print("5- chuan hoa cau \n" + text)
    text = bo_stopword(text)
    print("6- bo word \n" + text)
    return text


paragraph_test = (
    "ở việt nam rất tốt. tôi thích thời điểm 3.00 giờ. lúc đó rất đẹp."
)

output = tien_xu_li(paragraph_test)
