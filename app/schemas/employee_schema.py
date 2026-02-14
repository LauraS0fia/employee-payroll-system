from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    nombre: str
    sueldo: float
    dias_trabajados: int
    arl: int

    horas_extras_diurnas: int = 0
    horas_extras_nocturnas: int = 0
    horas_festivas_diurnas: int = 0
    horas_festivas_nocturnas: int = 0


class EmployeeUpdate(BaseModel):
    nombre: str | None = None
    sueldo: float | None = None
    dias_trabajados: int | None = None
    arl: int | None = None

    horas_extras_diurnas: int | None = None
    horas_extras_nocturnas: int | None = None
    horas_festivas_diurnas: int | None = None
    horas_festivas_nocturnas: int | None = None