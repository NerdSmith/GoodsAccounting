from src.models.ItemModel import ItemBase


class ItemSchema(ItemBase):
    id: int


class ItemSchemaCreate(ItemBase):
    pass


class ItemSchemaUpdate(ItemBase):
    pass
