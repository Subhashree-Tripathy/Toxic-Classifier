import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel

MAX_LEN = 128

# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained('./muril-base-cased')
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
# checkpoint_fpath = './best_model.pt'
checkpoint_fpath = './best_model_multi_lang_muril_V1.pt'

class BERTClass(torch.nn.Module):
    def __init__(self):
        super(BERTClass, self).__init__()
        self.bert_model = AutoModel.from_pretrained('./muril-base-cased')
        self.dropout = torch.nn.Dropout(0.3)        
        self.l1 = torch.nn.Linear(768, 64)
        self.bn1 = torch.nn.LayerNorm(64)
        self.d2 = torch.nn.Dropout(0.3)
        self.l2 = torch.nn.Linear(64, 1)
    
    def forward(self, input_ids, attn_mask, token_type_ids):
        output = self.bert_model(
            input_ids, 
            attention_mask=attn_mask, 
            token_type_ids=token_type_ids
        )
        output = self.dropout(output.pooler_output)

        output = self.l1(output)
        output = self.bn1(output)
        output = torch.nn.Tanh()(output)
        output = self.d2(output)
        output = self.l2(output)
        return output

model = BERTClass()
model.to(device)

checkpoint = torch.load(checkpoint_fpath,map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['state_dict'])

def predict(example):
    encodings = tokenizer.encode_plus(
      example,
      None,
      add_special_tokens=True,
      max_length=MAX_LEN,
      padding='max_length',
      return_token_type_ids=True,
      truncation=True,
      return_attention_mask=True,
      return_tensors='pt'
  )
    model.eval()
    with torch.no_grad():
        input_ids = encodings['input_ids'].to(device, dtype=torch.long)
        attention_mask = encodings['attention_mask'].to(device, dtype=torch.long)
        token_type_ids = encodings['token_type_ids'].to(device, dtype=torch.long)
        output = model(input_ids, attention_mask, token_type_ids)
        final_output = torch.sigmoid(output).cpu().detach().numpy().tolist()
        return 0 if final_output[0][0] < 0.4 else 1

    
#reads the file & adds a new pred col 
# dfTest = pd.read_csv('./Toxic_Comment_Classifier_Testdata - Sheet1 (1).csv')
# dfTest['bert-base-uncased']=[predict(i) for i in dfTest['Toxic Comments']]
# dfTest.to_csv('./res.csv',index = False)