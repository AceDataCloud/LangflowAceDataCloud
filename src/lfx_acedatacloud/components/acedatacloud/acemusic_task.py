"""ACE Music task reader."""

from lfx_acedatacloud.components.base import AceTaskComponent, task_inputs


class AceMusicRetrieveTaskComponent(AceTaskComponent):
    display_name = "ACE Music Retrieve Task by Ace Data Cloud"
    description = "Query the same ACE Music task through Ace Data Cloud without another paid generation."
    icon = "Music"
    documentation = "https://github.com/AceDataCloud/LangflowAceDataCloud/blob/main/guides/acemusic.md"
    service_name = "acemusic"
    inputs = task_inputs("acemusic")
