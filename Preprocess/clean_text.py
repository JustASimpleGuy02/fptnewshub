import pandas as pd
import unicodedata
import regex as re
from pyvi import ViTokenizer, ViPosTagger
import argparse
from tqdm import tqdm
from icecream import ic
import os
import os.path as osp

# dir_path = os.path.dirname(os.path.realpath(__file__))
# stopwords = open(osp.join(dir_path, 'stopword.txt'), 'r')
# stopwords_list = stopwords.read().split('\n')

bang_nguyen_am= [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                  ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                  ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                  ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                  ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                  ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                  ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                  ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                  ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                  ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                  ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                  ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]

bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']

nguyen_am_to_ids = {}
for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)
        
def chuan_hoa_unicode(text):
	text = unicodedata.normalize('NFC', text)
	return text

def chuan_hoa_dau_tu_tieng_viet(word):
    """
        Hàm này xử lý chuẩn hóa từng từ một, 
    sau khi chuẩn hóa từng từ thì sẽ chuân hóa từng câu sau 
    """ 
    if not is_valid_vietnam_word(word):
        return word
 
    chars = list(word)
    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
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
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
            return ''.join(chars)
        return word
 
    for index in nguyen_am_index:
        x, y = nguyen_am_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            # for index2 in nguyen_am_index:
            #     if index2 != index:
            #         x, y = nguyen_am_to_ids[chars[index]]
            #         chars[index2] = bang_nguyen_am[x][0]
            return ''.join(chars)
 
    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            # chars[nguyen_am_index[1]] = bang_nguyen_am[x][0]
        else:
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
        # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[2]]]
        # chars[nguyen_am_index[2]] = bang_nguyen_am[x][0]
    return ''.join(chars)

def is_valid_vietnam_word(word):
    chars = list(word)
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

def chuan_hoa_dau_cau_tieng_viet(sentence):
    """
        Chuyển câu tiếng việt về chuẩn gõ dấu kiểu cũ.
        :param sentence:
        :return:
        """
    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
        # print(cw)
        if len(cw) == 3:
            cw[1] = chuan_hoa_dau_tu_tieng_viet(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)

def tach_tu_tieng_viet(text):
	text = ViTokenizer.tokenize(text)
	return text

# Đưa về chữ viết thường 
def chuyen_chu_thuong(text):
	return text.lower()

# Xóa đi các dấu cách thừa, các từ không cần thiết cho việc phân loại vẳn bản 
def chuan_hoa_cau(text):
	text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',text)
	text = re.sub(r'\s+', ' ', text).strip()
	return text

def tien_xu_li(text):
	text = chuan_hoa_unicode(text)
	text = chuan_hoa_dau_cau_tieng_viet(text)
	text = tach_tu_tieng_viet(text)
	text = chuyen_chu_thuong(text)
	text = chuan_hoa_cau(text)

	return text

def bo_stopwords(text):
    text = text.split(' ')
    text = [t for t in text if t not in stopwords_list]
    return ' '.join(text)

def parse_args():
    parser = argparse.ArgumentParser(description="Clean text from csv file")
    parser.add_argument('ifile', help='input csv file')
    parser.add_argument('ofile', help='output csv file')
    parser.add_argument('-r', '--resume', action='store_true', help='resume from previous output csv file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    
    ifile = args.ifile
    ofile = args.ofile
    resume = args.resume
    
    if resume:
        out_df = pd.read_csv(ofile)
        
        remove_col = 'Unnamed: 0'

        if remove_col in out_df.columns.to_list():
            out_df.drop(columns=remove_col, inplace=True)
    else:
        out_df = pd.DataFrame(columns=['Link', 'Time', 'Cleaned_Content'])
    
    ### Read csv
    df = pd.read_csv(ifile)
    
    print('Number of links:', len(df))
    
    ### Save to output csv file
    for idx, row in tqdm(df.iterrows()):
        link = row.link
        
        if link in out_df['Link'].values:
            continue
        
        # Save every 300 intervals
        if idx % 300 == 1:  
            print('Current number of rows in new csv file:', len(out_df))
            print('Saving to csv...')
            out_df.to_csv(ofile, index=False)
        
        # Clean text with title
        try:
            content = row.title + '. ' + row.text
        except:
            if isinstance(row.title, float) and isinstance(row.text, float):
                # content = ''
                continue
            elif isinstance(row.title, float):
                content = row.text
            elif isinstance(row.text, float):
                content = row.title

            ic(row.title, row.text)
            
        cleaned_content = tien_xu_li(content)
        # cleaned_content = bo_stopwords(cleaned_content)
        
        # Add new row to output csv file
        out_df.loc[len(out_df.index)] = [row.link, row.time, cleaned_content]
    
