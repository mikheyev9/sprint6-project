
import json
import logging

from functional.testdata.test_param.film_param import ( # noqa
    AbstractDTO,
    MoviesList,
)
from functional.testdata.test_param.person_param import PersonsList # noqa
from functional.testdata.test_param.genre_param import GenresList # noqa


logger = logging.getLogger(__name__)


def load_data_from_json(index: str) -> AbstractDTO:
    file_path = f'functional/json_data/{index}.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                logger.warning(f"Файл {file_path} пуст.")
                return None
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при загрузке файла {file_path}: {str(e)}")
        return None
    model_class = AbstractDTO.get_subclasses().get(f"{index.lower()}list")
    if model_class:
        try:
            return model_class(**data).model_dump()
        except Exception as e:
            logger.error(
                f"Ошибка при создании экземпляра {model_class.__name__}: "
                f"{str(e)}"
            )
            return None

    logger.warning(f"Неизвестный индекс: {index}.")
    return None
