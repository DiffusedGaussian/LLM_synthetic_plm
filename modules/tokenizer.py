from tokenizers import Tokenizer, models, trainers, pre_tokenizers

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokinizers.Whitespace()

trainer = trainers.BpeTrainer(special_tokens=["<PAD>", "<UNK>", "<BOS>", "<EOS>"])
