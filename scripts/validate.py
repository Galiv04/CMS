import yaml
import sys
from pathlib import Path

REQUIRED_FIELDS = {
    "id": str,
    "version": str,
    "parameters": dict,
    "approvals": list
}

def validate_file(path: Path):
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            
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
