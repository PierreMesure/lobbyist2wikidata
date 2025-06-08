from enum import Enum
from pydantic import BaseModel, Field


class Status(Enum):
    CURRENT = "Nuvarande roll"
    PAST = "Tidigare roll"


class Role(BaseModel):
    title: str = Field(
        title="title",
        description="The position/role that the person has in the organisation. The name of the organisation shouldn't be in the title.",
    )
    organisation: str = Field(
        title="name",
        description="The name of the organisation. Be careful not to concatenate several organisations separated by commas",
    )
    status: Status = Field(
        title="status",
        description="Whether the role is current or past. If the word 'former' or 'tidigare' is mentioned, it is most probably past.",
    )


class PoliticalRole(Role):
    organisation: None = Field(
        title="name",
        description="For a political role, the organisation is the political party which is already provided in the associated field.",
    )
