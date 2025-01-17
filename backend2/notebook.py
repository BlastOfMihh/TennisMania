
import torch
import torch.nn as nn
from torch.nn import functional as F
import pickle


# hyperparameters
batch_size = 4 # how many independent sequences will we process in parallel?
block_size = 32 # what is the maximum context length for predictions?
max_iters = 40000
eval_interval = 100
learning_rate = 1e-3
device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu'
eval_iters = 200
n_embd = 64
n_head = 4
n_layer = 6
dropout = 0.2

score_size=3
# ------------
feel_count=16
feel_embd=32
# ------------


torch.manual_seed(1337)



import pandas as pd

#drive.mount('/content/drive')
#with open("/content/drive/MyDrive/LLm fighthing/karamazov.txt", "r", encoding="utf-8") as f:
#  text=f.read()

one_csv_path="./tt csv artificial.CSV"

df=pd.read_csv(one_csv_path)
df = df.drop(df.columns[0], axis=1)
df

hb_column = df.iloc[:, 0]
min_hb = hb_column.min()
max_hb = hb_column.max()
diff_hb = max_hb - min_hb + 1
print(min_hb, max_hb, max_hb-min_hb)



# The feel stuff
class FeelHead(nn.Module):
    """ one head of self-attention """
    def __init__(self, head_size):
        super().__init__()
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.key = nn.Linear(feel_embd, head_size, bias=False)

        self.value = nn.Linear(feel_embd, head_size, bias=False)

        self.feelings = torch.rand(feel_count, feel_embd).to(device)

        #self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B,T,C = x.shape
        q = self.query(x) # (B,T,C)

        k = self.key(self.feelings) # (f_cnt, C)
        k = k.expand(B, -1,-1) # (B, F_cnt, C)

        # compute attention scores ("affinities")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, F_cnt) -> (B, T, F_cnt)
        #wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, )
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # perform the weighted aggregation of the values
        v = self.value(self.feelings) # (f_cnt, C)
        v = v.expand(B,-1,-1) # (B, F_cnt, C)
        out = wei @ v # (B, T, F_cnt) @ (B, F_cnt, C) -> (B, T, C)
        return out


class MultiHeadFeeling(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([FeelHead(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out
    


class Head(nn.Module):
    """ one head of self-attention """
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x)   # (B,T,C)
        q = self.query(x) # (B,T,C)
        # compute attention scores ("affinities")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # perform the weighted aggregation of the values
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out

class MultiHeadAttention(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out

class FeedFoward(nn.Module):
    """ a simple linear layer followed by a non-linearity """

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    """ Transformer block: communication followed by computation """

    def __init__(self, n_embd, n_head, model_type):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        super().__init__()
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ln1 = nn.LayerNorm(n_embd)

        self.ffwd = FeedFoward(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

        self.model_type=model_type
        if model_type=='feel':
          self.mh_feel=MultiHeadFeeling(n_head, head_size)
          self.ln3 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        if self.model_type=='feel':
          x = x + self.mh_feel(self.ln3(x))
        x = x + self.ffwd(self.ln2(x))
        return x


# super simple bigram model
class BigramLanguageModel(nn.Module):

    def __init__(self, model_type):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Linear(score_size, n_embd) # changed this
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head, model_type=model_type) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd) # final layer norm
        self.lm_head = nn.Linear(n_embd, diff_hb+12+12)

    def forward(self, idx, targets=None):
        B, T, _= idx.shape
        idx=idx.to(torch.float32)
        # idx and targets are both (B,T,3) tensor of integers
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        logits = self.lm_head(x) # (B,T,3)

        if targets is None:
            loss = None

            logits_hb = logits[:, :, :diff_hb]
            logits_p1 = logits[:, :, diff_hb:diff_hb+12]
            logits_p2 = logits[:, :, diff_hb+12:diff_hb+12+12]
        else:
            B, T, C = logits.shape

            logits_hb = logits[:, :, :diff_hb].view(B*T, diff_hb)
            logits_p1 = logits[:, :, diff_hb:diff_hb+12].view(B*T, 12)
            logits_p2 = logits[:, :, diff_hb+12:diff_hb+12+12].view(B*T, 12)

            targets_hb = targets[:, :, 0:1].view(B*T)
            targets_p1 = targets[:, :, 1:2].view(B*T)
            targets_p2 = targets[:, :, 2:3].view(B*T)

            loss_hb = F.cross_entropy(logits_hb, targets_hb-torch.full((B*T,),min_hb))
            loss_p1 = F.cross_entropy(logits_p1, targets_p1)
            loss_p2 = F.cross_entropy(logits_p2, targets_p2)

            loss = loss_hb + loss_p1 + loss_p2


#            logits = logits.view(B*T, C)
#            targets = targets.view(B*T)

            #loss =  F.mse_loss(logits, targets) # changed this ?
            #loss = F.cross_entropy(logits, targets)
        return (logits_hb, logits_p1, logits_p2), loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            # crop idx to the last block_size tokens
            idx_cond = idx[:, -block_size:]
            # get the predictions
            (logits_hb, logits_p1, logits_p2), loss = self(idx_cond)
            # focus only on the last time step
            logits_hb = logits_hb[:, -1, :] # becomes (B, C)
            logits_p1 = logits_p1[:, -1, :] # becomes (B, C)
            logits_p2 = logits_p2[:, -1, :] # becomes (B, C)
            # apply softmax to get probabilities
            probs_hb = F.softmax(logits_hb, dim=-1) # (B, C)
            probs_p1 = F.softmax(logits_p1, dim=-1) # (B, C)
            probs_p2 = F.softmax(logits_p2, dim=-1) # (B, C)
            # sample from the distribution
            hb_next = torch.multinomial(probs_hb, num_samples=1) # (B, 1)
            p1_next = torch.multinomial(probs_p1, num_samples=1) # (B, 1)
            p2_next = torch.multinomial(probs_p2, num_samples=1) # (B, 1)

            idx_next = torch.stack([hb_next+min_hb,p1_next,p2_next], dim=-1)
            # breakpoint()
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx

model=BigramLanguageModel('regular')

def get_model():
    # Create a new instance of your model (with the same architecture)
    new_model = BigramLanguageModel('regular')

    # Load the saved weights
    new_model.load_state_dict(torch.load('model_weights.pth'))

    # Set the model to evaluation mode (optional but recommended)
    new_model.eval()
    return new_model