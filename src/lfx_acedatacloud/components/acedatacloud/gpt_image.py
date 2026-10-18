"""Gpt Image generation component."""

from lfx_acedatacloud.components.base import AceGenerationComponent, generation_inputs


class GPTImageGenerateComponent(AceGenerationComponent):
    display_name = "GPT Image Generate by Ace Data Cloud"
    description = "Generate GPT Image (GPTImage) images through Ace Data Cloud."
    icon = "Image"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/gpt-image.md"
    service_name = "gpt_image"
    inputs = generation_inputs("gpt_image")
