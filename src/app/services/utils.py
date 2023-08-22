from typing import TypeVar, Generic, Type

from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel

from src.app.services import mixins

ServiceInstance = TypeVar("ServiceInstance")


class Service(mixins.ServiceInstanceMixin[ServiceInstance], Generic[ServiceInstance]):
    pass


class UUIDService(mixins.UUIDServiceInstanceMixin[ServiceInstance], Service[ServiceInstance], Generic[ServiceInstance]):
    pass


BaseModel = TypeVar("BaseModel", bound=Model)
PydanticBaseModel = TypeVar("PydanticBaseModel", bound=PydanticModel)


class TortoiseService(Service[BaseModel], Generic[BaseModel, PydanticBaseModel]):
    pydantic_model: Type[PydanticBaseModel]

    async def get_instance_as_pydantic(self) -> PydanticBaseModel:
        self.validate_instance_filled()
        return await self.pydantic_model.from_tortoise_orm(self.instance)

    @classmethod
    def _model_fields(cls) -> set[str]:
        return cls.model._meta.fields

    async def create(self, **kwargs) -> BaseModel:
        self.instance = await self.model.create(**kwargs)
        return self.instance

    async def update(self, **kwargs) -> BaseModel:
        self.validate_instance_filled()
        attrs_for_update = {attr: value for attr, value in kwargs.items() if attr in self._model_fields()}
        for attr, value in attrs_for_update.items():
            setattr(self.instance, attr, value)
        await self.instance.save(update_fields=attrs_for_update.keys())
        return self.instance

    async def delete(self) -> BaseModel:
        self.validate_instance_filled()
        deleted_instance = self.instance
        await self.instance.delete()
        return deleted_instance
