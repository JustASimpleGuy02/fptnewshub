import unicodedata
import regex as re
from pyvi import ViTokenizer

bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
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

vowel_to_ids = {}
for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        vowel_to_ids[bang_nguyen_am[i][j]] = (i, j)

def is_valid_vietnam_word(word):
    chars = word.split()
    vowel_index = -1
    for index, char in enumerate(chars):
        x, y = vowel_to_ids.get(char, (-1, -1))
        if x != -1:
            if vowel_index == -1:
                vowel_index = index
            else:
                if index - vowel_index != 1:
                    return False
                vowel_index = index
    return True

# lowercase sentences
def to_lowercase(text):
    return text.lower()

# delete links
# normalize unicode
def normalize_unicode(text):
    text = unicodedata.normalize('NFC', text)
    return text

# delete redundant characters
# delete redundant spaces
def remove_redundant_characters(text):
    text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]', ' ', text )
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# normalize accented letters for each word
def normalize_accented_letters_for_each_word(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = word.split()
    dau_cau = 0
    index_of_vowel = []
    qu_or_gi =False

    for index, char in enumerate(chars):
        x, y = vowel_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9: #check qu
            if index != 0 and chars[index -1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5: #check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            index_of_vowel.append(index)
    if len(index_of_vowel) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = vowel_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = vowel_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
            return word
        return word

    for index in index_of_vowel:
        x, y - vowel_to_ids[chars[index]]
        if x == 4 or x == 8: # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            return ''.join(chars)

    if len(index_of_vowel) == 2:
        if index_of_vowel[-1] == len(chars) - 1:
            x, y = vowel_to_ids[chars[index_of_vowel[0]]]
            chars[index_of_vowel[0]] = bang_nguyen_am[x][dau_cau]
        else:
            x, y = vowel_to_ids[chars[index_of_vowel[1]]]
            chars[index_of_vowel[1]] = bang_nguyen_am[x][dau_cau]
    else:
        x, y = vowel_to_ids[chars[index_of_vowel[1]]]
        chars[index_of_vowel[1]] = bang_nguyen_am[x][dau_cau]
    return ''.join(chars)

# normalize accented letters for each sentence
def normalize_accented_letters_for_each_senence(sentence):
    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
        if len(cw) == 3:
            cw[1] = normalize_accented_letters_for_each_word(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)

# word tokenize
def word_tokenization(text):
    text = ViTokenizer.tokenize(text)
    return text

# delete teencode
# remove stopwords
with open('Preprocess/stopword.txt', 'r', encoding = 'utf-8') as f:
    stopword_list = f.read().split('\n')

def remove_stopwords(text):
    text = text.split()
    non_sw_text = []
    for word in text:
       if word not in stopword_list:
           non_sw_text.append(word)
    result = ' '.join([str(item) for item in non_sw_text])
    return result

def prepare_text(text):
    text = to_lowercase(text)
    text = normalize_unicode(text)
    text = remove_redundant_characters(text)
    text = normalize_accented_letters_for_each_senence(text)
    text = word_tokenization(text)
    text = remove_stopwords(text)
    return text