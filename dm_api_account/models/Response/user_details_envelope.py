from __future__ import annotations

import datetime
from enum import Enum
from typing import List, Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    )

from dm_api_account.models.Response.user_envelope import UserRole

class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None


class UserDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(None, description='Login')
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None)
    rating: Rating
    online: datetime.datetime = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime.datetime = Field(None)
    icq: str = Field(None)
    skype: str = Field(None)
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: InfoBbText | str = Field(None)
    settings: UserSettings | str= Field(None)

class UserSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    color_schema: ColorSchema | str = Field(None, alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings

class PagingSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    posts_per_page: int = Field(None, alias='postsPerPage')
    comments_per_page: int = Field(None, alias='commentsPerPage')
    topics_per_page: int = Field(None, alias='topicsPerPage')
    messages_per_page: int = Field(None, alias='messagesPerPage')
    entities_per_page: int = Field(None, alias='entitiesPerPage')

class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int

class InfoBbText(BaseModel):
    value: str = Field(None, alias='value')
    parse_mode: BbParseMode = Field(None, alias='parseMode')

class BbParseMode(Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'POST'
    CHAT = 'Chat'


class ColorSchema(Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'





