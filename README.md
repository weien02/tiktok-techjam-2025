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
docker-compose run --rm review-analyzer
```

3. Test Set Up

```bash
python test_setup.py
```
