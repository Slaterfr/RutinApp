from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr

class User(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    email : EmailStr
    password : str
    routines : list["Rutina"] = Relationship(back_populates="owner")

class Rutina(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    days_trained : int
    hours_trained : float
    days : list["DiaRutina"] = Relationship(back_populates="routine")
    owner_id : int | None = Field(default=None, foreign_key="user.id")
    owner : User | None = Relationship(back_populates="routines")

class DiaRutina(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    routine_id : int | None = Field(default=None, foreign_key="rutina.id")
    day_number : int
    day_name : str
    focus_area : str
    routine : Rutina | None = Relationship(back_populates="days")
    exercises : list["detalleEjercicio"] = Relationship(back_populates="day")

class detalleEjercicio(SQLModel, table=True):
    detail_id : int | None = Field(default=None, primary_key=True)
    excersise_id : int
    name : str 
    set_count : int
    rep_target : int
    rest_seconds : int
    weight_notes : str
    equipment_needed : str
    day : DiaRutina | None = Relationship(back_populates="exercises")
    day_id : int | None = Field(default=None, foreign_key="diarutina.id")







