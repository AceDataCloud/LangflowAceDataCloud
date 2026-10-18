"""Seedance generation component."""

from lfx_acedatacloud.components.base import AceGenerationComponent, generation_inputs


class SeedanceGenerateComponent(AceGenerationComponent):
    display_name = "Seedance Generate by Ace Data Cloud"
    description = "Generate Seedance videos through Ace Data Cloud."
    icon = "Clapperboard"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/seedance.md"
    service_name = "seedance"
    inputs = generation_inputs("seedance")
