import logging
from contextlib import suppress

from .typedefs import HonEntityDescription, HonOptionEntityDescription, T

_LOGGER = logging.getLogger(__name__)


def unique_entities(
    base_entities: tuple[T, ...],
    new_entities: tuple[T, ...],
) -> tuple[T, ...]:
    result = list(base_entities)
    existing_entities = [entity.key for entity in base_entities]
    entity: HonEntityDescription
    for entity in new_entities:
        if entity.key not in existing_entities:
            result.append(entity)
    return tuple(result)


def get_readable(
    description: HonOptionEntityDescription, value: float | str
) -> float | str:
    if description.option_list is not None:
        with suppress(ValueError):
            return description.option_list.get(int(value), value)
    return value
