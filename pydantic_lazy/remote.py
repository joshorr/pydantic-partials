# from typing import Iterator, Any
#
# from .lazy import LazyModel
# from .partial import PartialModel, _PartialMeta
#
#
# class Client[T: RemoteModel]:
#     def get(self, id: list[str] | None = None) -> Iterator:
#         yield from iter([])
#
#     def first(self, id: str | None = None):
#         return self.get()
#
#     def delete(self, obj: '_RemoteMeta'):
#         pass
#
#     def bulk_delete(self: ):
#         pass
#
#     def bulk_save(self):
#         pass
#
#
# # metaclass to make all fields in a model optional, useful for PATCH requests
# class _RemoteMeta(_PartialMeta):
#     def __new__(
#         cls, name: str, bases: tuple[type], namespaces: dict[str, Any], **kwargs
#     ):
#         # Create the class first...
#         cls: type[BaseModel] = super().__new__(cls, name, bases, namespaces, _PartialMeta__delay_rebuild=True, **kwargs)  # type: ignore
#
#         cls.model_fields.pop('client')
#         cls.model_rebuild(force=True)
#         return cls
#
#     @property
#     def client(cls) -> Client:
#         return Client()
#
#
# class RemoteModel(LazyModel, metaclass=_RemoteMeta):
#
#     client: Client
#
#     @property
#     def model_id(self) -> str:
#         raise NotImplementedError()
#
