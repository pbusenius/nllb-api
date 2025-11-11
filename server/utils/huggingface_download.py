from pathlib import Path


def huggingface_download(repository: str) -> str:
    """
    Summary
    -------
    get the local huggingface model path (models are pre-copied into image)

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
    
    # Models not found - raise error
    raise FileNotFoundError(
        f"Model {repository} not found in {cache_dir}. "
        f"Run 'make download-models' to download models."
    )
