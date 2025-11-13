import os
from pathlib import Path

from huggingface_hub import snapshot_download


def huggingface_download(repository: str) -> str:
    """
    Summary
    -------
    get the local huggingface model path, downloading if not found locally

    Parameters
    ----------
    repository (str) : the name of the Hugging Face repository

    Returns
    -------
    repository_path (str) : local path to the model
    """
    cache_dir = Path.home() / ".cache" / "huggingface"
    repo_name = repository.replace("/", "--")
    
    # Check hub format: hub/models--repo-name/snapshots/hash/
    hub_path = cache_dir / "hub" / f"models--{repo_name}" / "snapshots"
    if hub_path.exists():
        snapshots = [s for s in hub_path.iterdir() if s.is_dir()]
        if snapshots:
            return str(snapshots[0])
    
    # Check legacy format: models--repo-name/snapshots/hash/
    legacy_path = cache_dir / f"models--{repo_name}" / "snapshots"
    if legacy_path.exists():
        snapshots = [s for s in legacy_path.iterdir() if s.is_dir()]
        if snapshots:
            return str(snapshots[0])
    
    # Model not found locally - download if HUGGINGFACE_LOCAL_ONLY is not set
    huggingface_local_only = os.getenv("HUGGINGFACE_LOCAL_ONLY", "0")
    if huggingface_local_only in ("1", "true", "True"):
        raise FileNotFoundError(
            f"Model {repository} not found in {cache_dir}. "
            f"Run 'make download-models' to download models."
        )
    
    # Download the model
    try:
        model_path = snapshot_download(
            repo_id=repository,
            cache_dir=str(cache_dir),
        )
        return model_path
    except Exception as e:
        raise FileNotFoundError(
            f"Failed to download {repository}: {e}"
        ) from e
