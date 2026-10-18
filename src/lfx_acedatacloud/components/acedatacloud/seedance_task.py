"""Seedance task reader."""

from lfx_acedatacloud.components.base import AceTaskComponent, task_inputs


class SeedanceRetrieveTaskComponent(AceTaskComponent):
    display_name = "Seedance Retrieve Task by Ace Data Cloud"
    description = "Query the same Seedance task through Ace Data Cloud without another paid generation."
    icon = "Clapperboard"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/v0.1.3/guides/seedance.md"
    service_name = "seedance"
    inputs = task_inputs("seedance")
