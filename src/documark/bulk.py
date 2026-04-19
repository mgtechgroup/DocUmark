import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from documark.security import check_file
from documark.converters import convert_file

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".html", ".htm"}


def _collect_files(path: str, recursive: bool) -> list[str]:
    if os.path.isfile(path):
        return [path]
    files: list[str] = []
    if recursive:
        for root, _, fnames in os.walk(path):
            for fname in fnames:
                if os.path.splitext(fname)[1].lower() in SUPPORTED_EXTENSIONS:
                    files.append(os.path.join(root, fname))
    else:
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if os.path.isfile(fpath) and os.path.splitext(fname)[1].lower() in SUPPORTED_EXTENSIONS:
                files.append(fpath)
    return sorted(files)


def bulk_convert(
    path: str,
    output_dir: str = ".",
    recursive: bool = False,
    vt_api_key: str | None = None,
    max_workers: int = 4,
) -> dict:
    """
    Convert all supported files in path. Every file is security-checked first.
    Returns {"converted": list, "quarantined": list, "errors": list}.
    """
    files = _collect_files(path, recursive)
    converted: list[str] = []
    quarantined: list[str] = []
    errors: list[str] = []

    def _process(file_path: str) -> tuple[str, str]:
        security = check_file(file_path, vt_api_key)
        if not security["safe"]:
            return "quarantined", f"{file_path}: {security['reason']}"
        try:
            out = convert_file(file_path, output_dir)
            return "converted", out
        except Exception as exc:
            return "error", f"{file_path}: {exc}"

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_process, f): f for f in files}
        for future in as_completed(futures):
            status, detail = future.result()
            if status == "converted":
                converted.append(detail)
            elif status == "quarantined":
                quarantined.append(detail)
            else:
                errors.append(detail)

    return {"converted": converted, "quarantined": quarantined, "errors": errors}
