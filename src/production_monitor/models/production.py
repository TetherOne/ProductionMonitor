from sqlalchemy.orm import Mapped, mapped_column

from src.production_monitor.models.base import Base
from src.production_monitor.models.mixins.id_int_pk import IdIntPkMixin


class ProductionBatch(Base, IdIntPkMixin):
    is_closed: Mapped[bool] = mapped_column(default=False)
