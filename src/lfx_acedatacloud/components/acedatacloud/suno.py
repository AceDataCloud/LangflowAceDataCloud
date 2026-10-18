"""Suno generation component."""

from lfx_acedatacloud.components.base import AceGenerationComponent, generation_inputs


class SunoGenerateComponent(AceGenerationComponent):
    display_name = "Suno Generate by Ace Data Cloud"
    description = "Generate Suno music and audio through Ace Data Cloud."
    icon = "Music"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/suno.md"
    service_name = "suno"
    inputs = generation_inputs("suno")
