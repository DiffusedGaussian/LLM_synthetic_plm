This Repository is meant for training a tiny LLM to generate synthetic PLM Metadata from manufacturing parts based on a sample of real world metadata.

Structure 

LLM_synthetic_plm/
├── data/                    # Raw and intermediate datasets
│   ├── raw/                 # Unmodified source files (Excel, CSV)
│   ├── processed/           # Cleaned, formatted files (e.g. JSONL for training)
│   └── prompts/             # (Optional) prompt templates or manually crafted examples
│
├── modules/                # Core pipeline logic
│   ├── data_loader.py      # Excel reader, dataset class, JSONL export
│   ├── tokenizer.py        # Tokenizer training or loading logic (optional for now)
│   ├── model.py            # Your tiny GPT model definition (NanoGPT-like)
│   └── trainer.py          # Training loop or fine-tuning logic
│
├── scripts/                # CLI or runnable scripts
│   ├── prepare_data.py     # Converts Excel → JSONL
│   ├── train.py            # Trains a model from scratch or fine-tunes
│   └── generate.py         # Generates new metadata from the model
│
├── notebooks/              # Dev exploration (e.g., prompt crafting, quick tests)
│   └── data_loader_test.ipynb
│
├── tests/                  # Optional pytest or manual test scripts
│   └── test_data_loader.py
│
├── models/                 # Saved checkpoints (e.g. PyTorch .bin or Hugging Face format)
│
├── outputs/                # Generated data, sample outputs, eval results
│
├── README.md
├── requirements.txt
└── config.yaml             # (Optional) shared config for paths, params, etc.