from enum import Enum


class SwedishPoliticalParty(Enum):
    """
    Enum for Swedish political parties in the parliament.
    """

    SOCIALDEMOKRATERNA_S = "Socialdemokraterna (S)"
    MODERATERNA_M = "Moderaterna (M)"
    SVERIGEDEMOKRATERNA_SD = "Sverigedemokraterna (SD)"
    CENTERPARTIET_C = "Centerpartiet (C)"
    VANSTERPARTIET_V = "Vänsterpartiet (V)"
    LIBERALERNA_L = "Liberalerna (L)"
    KRISTDEMOKRATERNA_KD = "Kristdemokraterna (KD)"
    MILJOPARTIET_MP = "Miljöpartiet (MP)"
    ANNAT = "Annat"
    INGET = "Inget parti"

    @classmethod
    def list_values(cls):
        values = {}

        for party in cls:
            value = party.value
            if "(" in value:
                name, initial = value.split(" ")
                values[party.name] = [initial, name.strip()]
                if initial == "L":
                    values[party.name].extend(["(FP)", "Folkpartiet"])

        return values

    @classmethod
    def help_text(cls):
        values = SwedishPoliticalParty.list_values()
        parts = []

        for value in values:
            parts.append(f"{values[value][0]} for {values[value][1]}")

        return ", ".join(parts)
