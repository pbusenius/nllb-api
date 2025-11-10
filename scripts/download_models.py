#!/usr/bin/env python3
"""Download models to local cache and copy to models/ directory for Docker builds."""

import os
import shutil
import sys

from huggingface_hub import hf_hub_download, snapshot_download


def main() -> None:
    """Download models and copy to models/ directory."""
    cache_dir = os.path.expanduser("~/.cache/huggingface")

    print("Downloading models to local cache...")
    try:
        # Download translation model
        print("Downloading translation model...")
        translation_path = snapshot_download("winstxnhdw/nllb-200-distilled-1.3B-ct2-int8", cache_dir=cache_dir)
        print(f"Translation model downloaded to: {translation_path}")

        # Download language detection model
        print("Downloading language detection model...")
        lang_path = hf_hub_download("facebook/fasttext-language-identification", "model.bin", cache_dir=cache_dir)
        print(f"Language detection model downloaded to: {lang_path}")

        print(f"Models downloaded successfully to {cache_dir}")

        # Copy only the specific models we need to models/ directory
        print("Copying to models/ directory...")
        
        # Create models directory structure
        models_dir = "models"
        if os.path.exists(models_dir):
            shutil.rmtree(models_dir)
        os.makedirs(models_dir)
        
        # Copy only the specific model directories we need
        # Translation model: winstxnhdw/nllb-200-distilled-1.3B-ct2-int8
        # Check both hub/ format and legacy format
        translation_model_cache_hub = os.path.join(cache_dir, "hub", "models--winstxnhdw--nllb-200-distilled-1.3B-ct2-int8")
        translation_model_cache_legacy = os.path.join(cache_dir, "models--winstxnhdw--nllb-200-distilled-1.3B-ct2-int8")
        
        if os.path.exists(translation_model_cache_hub):
            print(f"Copying translation model from {translation_model_cache_hub}...")
            os.makedirs(os.path.join(models_dir, "hub"), exist_ok=True)
            shutil.copytree(translation_model_cache_hub, os.path.join(models_dir, "hub", "models--winstxnhdw--nllb-200-distilled-1.3B-ct2-int8"))
            print("Translation model copied successfully")
        elif os.path.exists(translation_model_cache_legacy):
            print(f"Copying translation model from {translation_model_cache_legacy}...")
            shutil.copytree(translation_model_cache_legacy, os.path.join(models_dir, "models--winstxnhdw--nllb-200-distilled-1.3B-ct2-int8"))
            print("Translation model copied successfully")
        else:
            print(f"ERROR: Translation model not found at {translation_model_cache_hub} or {translation_model_cache_legacy}", file=sys.stderr)
            sys.exit(1)
        
        # Language detection model: facebook/fasttext-language-identification
        # Check both hub/ format and legacy format
        lang_model_cache_hub = os.path.join(cache_dir, "hub", "models--facebook--fasttext-language-identification")
        lang_model_cache_legacy = os.path.join(cache_dir, "models--facebook--fasttext-language-identification")
        
        if os.path.exists(lang_model_cache_hub):
            print(f"Copying language detection model from {lang_model_cache_hub}...")
            os.makedirs(os.path.join(models_dir, "hub"), exist_ok=True)
            shutil.copytree(lang_model_cache_hub, os.path.join(models_dir, "hub", "models--facebook--fasttext-language-identification"))
            print("Language detection model copied successfully")
        elif os.path.exists(lang_model_cache_legacy):
            print(f"Copying language detection model from {lang_model_cache_legacy}...")
            shutil.copytree(lang_model_cache_legacy, os.path.join(models_dir, "models--facebook--fasttext-language-identification"))
            print("Language detection model copied successfully")
        else:
            print(f"ERROR: Language detection model not found at {lang_model_cache_hub} or {lang_model_cache_legacy}", file=sys.stderr)
            sys.exit(1)
        
        print("All models copied to models/ directory")

    except Exception as e:
        print(f"Error downloading models: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

