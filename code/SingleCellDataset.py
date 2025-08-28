import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class SingleCellDataset(Dataset):
    def __init__(self, x_, y_):
        super().__init__()
        x_ = np.array(x_)*10 # avoid small value problems
        x_ = np.expand_dims(x_, 1)
        self.x = x_
        self.y = np.array(y_).reshape(-1,1)  

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return torch.from_numpy(self.x[idx]).float(), torch.from_numpy(self.y[idx]).float()