from src.models.PlaceModel import PlaceBase


class PlaceSchema(PlaceBase):
    id: int


class PlaceSchemaCreate(PlaceBase):
    pass


class PlaceSchemaUpdate(PlaceBase):
    pass


class WeightedPlaceSchema(PlaceSchema):
    current_weight: float = 0
