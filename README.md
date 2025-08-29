# Set Up

## Directory Structure

```bash
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── workspace/
│   ├── test_setup.py
│   ├── src/
│   ├── data/
└── ~/.cache/huggingface/        # Hugging Face model & dataset cache on host
```

## Building and Running Docker

Make sure you have Docker Desktop installed and open.

1. Build Docker Image

```bash
docker-compose build
```

2. Run Docker Container

```bash
docker-compose run --rm review-analyzer ## --rm flag removes the container when it stops
```

To stop the container `ctrl + D`

3. Test Set Up

```bash
python test_setup.py
```

You should see something similar to below (if you have GPU):

```powershell
=== Python & Library Check ===
Python version: 3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0]
numpy version: 1.26.4 (expected 1.26.4)
pandas version: 2.1.1 (expected 2.1.1)
scikit-learn is not installed!
transformers version: 4.35.0 (expected 4.35.0)
huggingface_hub version: 0.16.4 (expected 0.16.4)
datasets version: 2.13.1 (expected 2.13.1)

=== GPU Check ===
GPU available: True
GPU name: NVIDIA GeForce RTX 4060 Laptop GPU
CUDA version: 12.8

=== Hugging Face Model Test ===
Loading Hugging Face model 'distilbert-base-uncased-finetuned-sst-2-english' on cuda...
Downloading tokenizer_config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████| 48.0/48.0 [00:00<00:00, 383kB/s]
Downloading config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 629/629 [00:00<00:00, 5.05MB/s]
Downloading vocab.txt: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 232k/232k [00:00<00:00, 16.1MB/s]
/usr/local/lib/python3.11/dist-packages/transformers/utils/generic.py:309: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
Downloading model.safetensors: 100%|█████████████████████████████████████████████████████████████████████████████████████████████| 268M/268M [00:07<00:00, 36.9MB/s]
Model 'distilbert-base-uncased-finetuned-sst-2-english' loaded successfully.
Test inference successful. Output logits: tensor([[ 1.7403, -1.5810]], device='cuda:0', grad_fn=<AddmmBackward0>)
```

