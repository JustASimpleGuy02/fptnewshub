import pandas as pd
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
from Model.preprocess import prepare_text

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


def inference(sentence):
    input_ids = torch.tensor([tokenizer.encode(sentence)]).to(device)
    with torch.no_grad():
        out = model(input_ids)
        out = out.logits.softmax(dim=-1)
        
    result = out.cpu().squeeze()
    result = torch.argmax(result).item()
    
    return labels[result]

  
def sentiment(row):
    temp_data = extract_value(row.text)
    temp_data.append(prepare_text(row.title))
    
    if len(temp_data)==0:
        return "Unknown"
    
    neg = []
    for sentence in temp_data:
        if sentence != "":
            try:
                neg.append(sentiment(sentence))
            except:
                continue
        else:
            neg.append(0)
    return 0




if __name__ == '__main__':
    print(inference("Tôi đẹp trai"))
    