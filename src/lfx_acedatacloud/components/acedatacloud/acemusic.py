"""ACE Music generation component."""

from lfx_acedatacloud.components.base import AceGenerationComponent, generation_inputs


class AceMusicGenerateComponent(AceGenerationComponent):
    display_name = "ACE Music Generate by Ace Data Cloud"
    description = "Generate songs from a musical idea with an ACE Music model."
    icon = "Music"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/guides/acemusic.md"
    service_name = "acemusic"
    inputs = generation_inputs("acemusic")
