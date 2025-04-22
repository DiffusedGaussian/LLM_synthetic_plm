import pandas as pd 

from torch.utils.data import Dataset, DataLoader

def load_excel_as_dicts(file_path:str) -> list:
    df = pd.read_excel(file_path, engine='openpyxl')
    df.fillna("", inplace=True) # clean missing values
    return df.to_dict(orient='records')

class ExcelJSONDataset(Dataset):
    def __init__(self, file_path:str, tokenizer = None, format_as_string=True):
        self.entries = load_excel_as_dicts(file_path)
        self.tokenizer = tokenizer 
        self.format_as_string = format_as_string
        
    def __len__(self):
        return len(self.entries)
    
    def __getitem__(self, idx):
        data = self.entries[idx]
        
        if self.format_as_string:
            # Flatten into string for LLM-style training
            text = " | ".join(f"{k}: {v}" for k, v in data.items())
            if self.tokenizer:
                return self.tokenizer(text, return_tensors='pt', padding="max_length", truncation=True)
            return text

        return data # JSON-style dictionary output 
    
def get_dataloader(file_path: str, 
                   tokenizer = None, 
                   batch_size: int = 8, 
                   shuffle: bool =True, 
                   format_as_string: bool = True)-> DataLoader:
    dataset = ExcelJSONDataset(file_path, tokenizer = tokenizer, format_as_string=format_as_string)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    
