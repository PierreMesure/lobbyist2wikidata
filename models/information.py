from pydantic import BaseModel, Field
from models.swedish_political_party import SwedishPoliticalParty
from models.role import PoliticalRole, Role


class Information(BaseModel):
    political_roles: list[PoliticalRole] = Field(
        title="political_roles",
        description="A list of political roles. It could be minister, riksdagsledamot, partisekreterare, partiledare...",
    )
    political_party: SwedishPoliticalParty = Field(
        title="political_party",
        description=f"The name of the political party. It should be mentioned once but people usually keep their political affiliation for their whole career so unless specified, the identified party applies to all the political roles. Political parties are often named with their initials between parentheses, e.g. {SwedishPoliticalParty.list_values()}.",
    )
    other_roles: list[Role] = Field(
        title="other_roles",
        description="A list of non-political roles, for instance at companies, pressure groups or in government in a non-political position",
    )
