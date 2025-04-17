import yaml
import sys
from pathlib import Path
import chardet  # Libreria per rilevare la codifica

REQUIRED_FIELDS = {
    "id": str,
    "version": str,
    "parameters": dict,
    "approvals": list
}

def detect_encoding(file_path):
    """Rileva la codifica del file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def validate_file(path: Path):
    try:
        # Rileva la codifica del file
        encoding = detect_encoding(path)
        
        # Leggi il file con la codifica rilevata
        with open(path, encoding=encoding) as f:
            data = yaml.safe_load(f)
            
        # Valida i campi richiesti
        for field, dtype in REQUIRED_FIELDS.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(data[field], dtype):
                raise TypeError(f"{field} must be {dtype.__name__}")
                
        print(f"Validation passed: {path}")
        return True
    except Exception as e:
        print(f"::error file={path},line=1::Validation failed: {str(e)}")
        return False

if __name__ == "__main__":
    exit_code = 0
    for filepath in sys.argv[1:]:
        if not validate_file(Path(filepath)):
            exit_code = 1
    sys.exit(exit_code)
