"""Happy Horse generation component."""

from lfx_acedatacloud.components.base import AceGenerationComponent, generation_inputs


class HappyHorseGenerateComponent(AceGenerationComponent):
    display_name = "Happy Horse Generate by Ace Data Cloud"
    description = "Generate Happy Horse (HappyHorse) videos through Ace Data Cloud."
    icon = "Clapperboard"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/happy-horse.md"
    service_name = "happy_horse"
    inputs = generation_inputs("happy_horse")
