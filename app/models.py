from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    address: Optional[dict] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[dict] = None


class Address(BaseModel):
    id: int
    uid: int | str
    city: Optional[str] = None
    street_name: Optional[str] = None
    street_address: Optional[str] = None
    secondary_address: Optional[str] = None
    building_number: Optional[int] = None
    mail_box: Optional[str] = None
    community: Optional[str] = None
    zip_code: Optional[str] = None
    zip: Optional[int] = None
    postcode: Optional[str] = None
    time_zone: Optional[str] = None
    street_suffix: Optional[str] = None
    city_suffix: Optional[str] = None
    city_prefix: Optional[str] = None
    state: Optional[str] = None
    state_abbr: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    full_address: Optional[str] = None


class CreditCard(BaseModel):
    id: int
    uid: int | str
    credit_card_number: Optional[str] = None
    credit_card_expiry_date: Optional[str] = None
    credit_card_type: Optional[str] = None
