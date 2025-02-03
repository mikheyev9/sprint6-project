import uuid


def generate_film():
    return {
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-65b69f4e3f95', 'name': 'Action'},
            {'id': 'fb111f22-121e-44a7-b78f-b14591810fbf', 'name': 'Sci-Fi'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'directors_names': ['John', 'Kayn'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'directors': [
            {'id': 'd586b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'full_name': 'John'},
            {'id': 'h8111f22-121e-44a7-b78f-b19191810fbf', 'full_name': 'Kayn'}
        ],
        'actors': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'full_name': 'Ann'},
            {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'full_name': 'Bob'}
        ],
        'writers': [
            {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'full_name': 'Ben'},
            {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'full_name': 'Howard'}
        ]
    }


def generate_films():
    return [generate_film() for _ in range(60)]