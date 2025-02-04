import uuid


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