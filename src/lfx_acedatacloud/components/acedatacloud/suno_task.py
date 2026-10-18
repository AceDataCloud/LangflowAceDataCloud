"""Suno task reader."""

from lfx_acedatacloud.components.base import AceTaskComponent, task_inputs


class SunoRetrieveTaskComponent(AceTaskComponent):
    display_name = "Suno Retrieve Task by Ace Data Cloud"
    description = "Query the same Suno task through Ace Data Cloud without another paid generation."
    icon = "Music"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/suno.md"
    service_name = "suno"
    inputs = task_inputs("suno")
