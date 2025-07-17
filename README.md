# LLM Synthetic PLM

Generate realistic **Product‑Lifecycle‑Management (PLM) metadata** from small, messy manufacturing datasets using a lightweight local language‑model.

---

## 🚀 Why this repo?

Manufacturing companies hold years of Bills‑of‑Material, PDFs, CAD drawings, and ERP exports—but these files are scattered, inconsistent, and rarely machine‑readable.  Fine‑tuned language models can hallucinate when trained on tiny, noisy samples.  **LLM Synthetic PLM** tackles both problems by

1. **Ingesting unstructured sources** (Excel, CSV, PDFs, legacy PLM dumps)
2. **Profiling**  with GPT‑4o api calls to draft a JSON cleaning plan based on column stats
3. **Applying deterministic** pandas transforms (rename, cast, impute, validate) driven by that plan
4. **Exporting** clean, audit‑ready JSONL for analytics, reporting, or downstream model work

---

## 🗂 Repository Layout

```text
LLM_synthetic_plm/
├── data/
│   ├── raw/          # Unmodified source files (Excel, CSV, PDFs)
│   ├── processed/    # Cleaned, normalised JSONL ready for training
│   └── prompts/      # Prompt templates or few‑shot examples
│
├── modules/
│   ├── data_loader.py   # Parsers & validators for tabular + PDF + PLM exports
│   ├── tokenizer.py     # Builds or loads a domain tokenizer (optional)
│   ├── model.py         # NanoGPT‑style TinyGPT architecture
│   └── trainer.py       # Training / fine‑tuning loop with Lightning
│
├── scripts/
│   ├── prepare_data.py  # CLI: Excel/PDF → JSONL
│   ├── train.py         # CLI: train or fine‑tune TinyGPT
│   └── generate.py      # CLI: emit synthetic metadata → JSON
│
├── notebooks/           # Rapid experiments & EDA
├── tests/               # pytest based unit tests
├── models/              # Saved checkpoints (HF or safetensors)
├── outputs/             # Generated samples & evaluation reports
├── config.yaml          # Centralised paths + hyper‑parameters
└── requirements.txt
```

---

## ✨ Key Features

| Capability                    | Details                                                                                                  |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Multi‑format ingestion**    | Parse Excel (.xls/.xlsx), CSV, PDF tables, and generic PLM XML/JSON dumps via a unified `DataLoader` API |
| **Schema‑aware cleaning**     | Automatic header mapping, unit conversion, duplicate collapse, and referential‑integrity checks          |
| **TinyGPT backbone**          | 2‑8 M parameter model; train on consumer GPU / CPU in minutes                                            |
| **Prompt‑oriented training**  | Supports instruction‑tuning and few‑shot augmentation to reduce hallucinations                           |
| **Deterministic JSON output** | Generates records conforming to a strict JSON schema (see `schemas/plm.json`)                            |
| **Evaluation suite**          | Bleu/BERTScore, schema‑conformance, and real‑world plausibility checks                                   |

---

## 🔧 Quickstart

1. **Clone & install**

   ```bash
   git clone https://github.com/<you>/LLM_synthetic_plm.git
   cd LLM_synthetic_plm
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Prepare data**
   Place your messy Excel or PDF files in `data/raw/` and run:

   ```bash
   python scripts/prepare_data.py \
       --src data/raw/*.xlsx data/raw/*.pdf \
       --dst data/processed/plm_train.jsonl
   ```
3. **Train / fine‑tune**

   ```bash
   python scripts/train.py \
       --config config.yaml \
       --data data/processed/plm_train.jsonl \
       --save_dir models/tinygpt_plm
   ```
4. **Generate synthetic metadata**

   ```bash
   python scripts/generate.py \
       --ckpt models/tinygpt_plm/best.ckpt \
       --n 1000 \
       --out outputs/synthetic_plm.jsonl
   ```

*Result:* `outputs/synthetic_plm.jsonl` contains valid, diverse PLM rows ready for analytics, RAG pipelines, or further model pre‑training.

---

## ⚙️ Configuration

All hyper‑parameters live in `config.yaml`:

```yaml
model:
  n_layers: 6
  n_heads: 6
  d_model: 384
training:
  batch_size: 64
  max_tokens: 128
  lr: 3e‑4
  epochs: 8
```

Override any value via CLI flags, e.g. `--training.epochs 12`.

---

## 🧩 Extending the Repo

* **Additional file types**: add a new parser class to `modules/data_loader.py` and register it.
* **Bigger models**: swap `model.py` for a Hugging Face architecture; config stays intact.
* **Structured validation**: extend `schemas/plm.json` and update `tests/` for new fields.

---

## 🛡️ License

Apache 2.0—free for commercial and research use. See `LICENSE`.

---

## 🤝 Contributing

PRs & issues are welcome!  Please run `pre‑commit` and `pytest` before opening a pull request.

---

## 🌐 Links & Inspiration

* [NanoGPT](https://github.com/karpathy/nanogpt)
* [LangChain PDF Loader](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf)
* [Hugging Face Datasets](https://huggingface.co/docs/datasets)

---

*Happy synthetic manufacturing!*
