from typing import List, Dict, Any
from functional.utils.load_json import load_data_from_json


GENRES_DATA: Dict[str, List[Dict[str, Any]]] = load_data_from_json(
    'genres'
)
