import sys
import importlib
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def check_python_version():
    print(f"Python version: {sys.version}")

def check_libraries():
    libraries = {
        "numpy": "1.26.4",
        "pandas": "2.1.1",
        "scikit-learn": "1.3.1",
        "transformers": "4.35.0",
        "huggingface_hub": "0.16.4",
        "datasets": "2.13.1",
    }
    for lib, expected_version in libraries.items():
        try:
            module = importlib.import_module(lib)
            installed_version = getattr(module, "__version__", "unknown")
            print(f"{lib} version: {installed_version} (expected {expected_version})")
        except ImportError:
            print(f"{lib} is not installed!")

def check_gpu():
    gpu_available = torch.cuda.is_available()
    print(f"GPU available: {gpu_available}")
    if gpu_available:
        print(f"GPU name: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")

def test_huggingface_model():
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        print(f"Loading Hugging Face model '{model_name}' on {device}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="/root/.cache/huggingface")
        model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir="/root/.cache/huggingface")
        model.to(device)
        print(f"Model '{model_name}' loaded successfully.")
        
        # Run a quick inference
        inputs = tokenizer("This is a test review.", return_tensors="pt").to(device)
        outputs = model(**inputs)
        print("Test inference successful. Output logits:", outputs.logits)
    except Exception as e:
        print(f"Error loading or running Hugging Face model: {e}")

if __name__ == "__main__":
    print("=== Python & Library Check ===")
    check_python_version()
    check_libraries()
    print("\n=== GPU Check ===")
    check_gpu()
    print("\n=== Hugging Face Model Test ===")
    test_huggingface_model()
