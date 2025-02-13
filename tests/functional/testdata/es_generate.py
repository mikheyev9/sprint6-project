from typing import List, Dict, Any

from functional.utils.load_json import load_data_from_json

MOVIES_DATA: Dict[str, List[Dict[str, Any]]] = load_data_from_json('movies')
GENRES_DATA: Dict[str, List[Dict[str, Any]]] = load_data_from_json(
    'genres'
)
PERSONS_DATA: Dict[str, List[Dict[str, Any]]] = load_data_from_json(
    'persons'
)
