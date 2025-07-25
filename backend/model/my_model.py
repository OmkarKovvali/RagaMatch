import torch
import torch.nn as nn

class Attention(nn.Module):
    def __init__(self, feature_dim):
        super(Attention, self).__init__()
        self.attention = nn.Linear(feature_dim, 1)
    def forward(self, lstm_out):
        scores = torch.tanh(self.attention(lstm_out))  # (batch, seq_len, 1)
        weights = torch.softmax(scores, dim=1)         # (batch, seq_len, 1)
        context = (weights * lstm_out).sum(dim=1)      # (batch, feature_dim)
        return context

class RagaTDNNLSTMAttention(nn.Module):
    def __init__(self, input_size, time_steps, num_classes):
        super(RagaTDNNLSTMAttention, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=input_size, out_channels=64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(64)
        self.pool1 = nn.MaxPool1d(2)  # halves time_steps
        self.lstm = nn.LSTM(input_size=64, hidden_size=256, batch_first=True)
        self.attention = Attention(256)
        self.fc1 = nn.Linear(256, 256)
        self.drop1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = torch.relu(x)
        x = self.pool1(x)               # (batch, 64, 650)
        x = x.permute(0, 2, 1)          # (batch, 650, 64)
        x, _ = self.lstm(x)
        x = self.attention(x)
        x = torch.relu(self.fc1(x))
        x = self.drop1(x)
        return self.fc2(x)
