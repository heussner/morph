import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader

from tqdm import tqdm

class trainTest():
    def __init__(self, model, trainDataset, testDataset, batchSize, epochs):
        super().__init__()
        self.model = model
        self.trainLoader = DataLoader(trainDataset, batchSize, shuffle=True)
        self.testLoader = DataLoader(testDataset, batchSize, shuffle=False)
        self.epochs = epochs
    
    def train(self):
        model = self.model.float()
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.0001)
        train_loss = []
        test_loss = []
        for i, epoch in tqdm(enumerate(range(self.epochs))):
            total_loss = 0.0
            for inputs, targets in self.trainLoader:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            train_loss.append(total_loss)
            total_loss = 0.0
            for inputs, targets in self.testLoader:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                total_loss += loss.item()
            test_loss.append(total_loss)
        self.trainLoss = train_loss
        self.testLoss = test_loss
        self.trainedModel = model
    
    def test(self):
        model = self.trainedModel.eval()
        predictions = []
        for inputs, targets in self.testLoader:
            outputs = model(inputs)
            predictions+=list(outputs.detach())
        self.predictions = np.array(predictions).flatten()
