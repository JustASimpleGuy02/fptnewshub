import pandas as pd
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from Model.preprocess import prepare_text
import numpy as np

device = 'cuda' if torch.cuda.is_available() else 'cpu'
labels = {
    0: 'Negative',
    1: 'Positive',
    2: 'Neutral'
}

model = RobertaForSequenceClassification.from_pretrained("wonrax/phobert-base-vietnamese-sentiment").to('cuda')
tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

def extract_value(text):
    res = []
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        sentences = paragraph.split(". ")
        if len(sentences) >=3:
            res.append(prepare_text(sentences[0]))
            res.append(prepare_text(sentences[len(sentences)-1]))
        elif len(sentences) == 2:
            res.append(prepare_text(sentences[0]))
            res.append(prepare_text(sentences[1]))
        else:
            res.append(prepare_text(sentences[0]))
    return res


# def inference(sentence):
#     input_ids = torch.tensor([tokenizer.encode(sentence)]).to(device)
#     with torch.no_grad():
#         out = model(input_ids)
#         out = out.logits.softmax(dim=-1)
        
#     result = out.cpu().squeeze()
#     result = torch.argmax(result).item()

#     return labels[result]

def inference(sentence):
    input_ids = torch.tensor([tokenizer.encode(sentence)]).to('cuda')
    with torch.no_grad():
        out = model(input_ids)
        out = out.logits.softmax(dim=-1).tolist()
    return out[0]

  
def sentiment_prob(row):
    temp_data = extract_value(row.text)
    temp_data.append(prepare_text(row.title))
    
    if len(temp_data)==0:
        return "Unknown"
    
    neg = []
    for sentence in temp_data:
        if sentence != "":
            try:
                neg.append(inference(sentence))
            except:
                neg.append([0,0,0])
        else:
            neg.append([0,0,0])
    neg = np.array(neg)
    res = np.sum(neg, 0)
    temp_data_length = len(temp_data)  # Obtain the length of temp_data
    res = np.divide(res, temp_data_length)  # Perform division with the length
    return res


def sentiment(row):
    probs = sentiment_prob(row)
    result = np.argmax(probs)
    return labels[result]


if __name__ == '__main__':
    df = pd.DataFrame(columns=["text", "title"])
    df.loc[len(df.index)] = ["Tôi đẹp trai.", "Bạn xấu òm."]
    
    row = df.loc[0]
    print(sentiment(row))
    
