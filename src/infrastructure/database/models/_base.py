
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class _Base(DeclarativeBase):

    __abstract__: bool = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        table_name = cls.__name__
        if table_name.endswith("y"):
            table_name = table_name[:-1] + "ie"
        result = table_name[0] + "".join(map(lambda x: "_" + x if x.istitle() else x, table_name[1:]))
        return f"{result.lower()}s"

    data: Mapped[dict] = mapped_column(
        JSONB,
        server_default="{}",
        default={},
        comment="Дополнительные данные",
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
