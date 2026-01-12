def detect_type(filename: str) -> str:
    fn = filename.lower()
    if fn.endswith(".pdf"):
        return "pdf"
    if fn.endswith((".png", ".jpg", ".jpeg")):
        return "image"
    return "unknown"
