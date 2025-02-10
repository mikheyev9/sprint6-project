import uuid
from typing import List, Dict, Any
from functional.utils.load_json import load_data_from_json


def generate_person():
    return {
        'id': str(uuid.uuid4()),
        'full_name': 'Tom Jerry',
        'films': [
            {'id': '1236b8ff-3c82-4d31-ad8e-65b69f4e3f95', 'roles': ['actor']},
            {'id': '1231f22d-121e-44a7-b78f-b14591810fbf', 'roles': ['director']}
        ],
    }


def generate_persons():
    return [generate_person() for _ in range(60)]


#  Генерацию функции не стал убирать, чтобы если что вдруг сравнить формат к
#  и если все ок то убрать(вдруг я где то косякнул))


PERSONS_DATA: Dict[str, List[Dict[str, Any]]] = load_data_from_json(
    'persons'
)
