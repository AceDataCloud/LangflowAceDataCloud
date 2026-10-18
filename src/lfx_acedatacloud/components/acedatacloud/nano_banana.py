"""Nano Banana generation component."""

from lfx_acedatacloud.components.base import AceGenerationComponent, generation_inputs


class NanoBananaGenerateComponent(AceGenerationComponent):
    display_name = "Nano Banana Generate by Ace Data Cloud"
    description = "Generate Nano Banana (NanoBanana) images through Ace Data Cloud."
    icon = "Image"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/nano-banana.md"
    service_name = "nano_banana"
    inputs = generation_inputs("nano_banana")
