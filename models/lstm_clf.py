import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence

from .config import LSTMConfig


class LSTM_Classifier(nn.Module):
    def __init__(self, vocab_size):
        super(LSTM_Classifier, self).__init__()
        self.emb_size = LSTMConfig.emb_size
        self.hidden_size = LSTMConfig.hidden_size
        self.vocab_size = vocab_size

        self.embedding = nn.Embedding(vocab_size, self.emb_size)
        self.lstm = nn.LSTM(self.emb_size, self.hidden_size,
                            bidirectional=True, batch_first=True)
        self.linear = nn.Linear(self.hidden_size*2, 1)

    def forward(self, sentences, lengths):

        emb = self.embedding(sentences)
        packed_seq = pack_padded_sequence(emb, lengths, batch_first=True)
        _, (h, _) = self.lstm(packed_seq)
        # h: [n_layer * num_directions, batch, hidden_size]
        hidden = torch.cat([h[0], h[1]], dim=1)  # [batch, hidden_size*2]
        out = self.linear(hidden)  # [B, 1]

        return out

    def init_embedding(self, embedding):
        self.embedding.weight.data = embedding
