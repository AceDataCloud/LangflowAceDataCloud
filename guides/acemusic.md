# ACE Music for Langflow

From a checkout containing these components, run `python -m pip install ./packages/acemusic` in the Langflow environment, restart the server, and search Components for **ACE Music**. This registers the standalone Generate and Retrieve Task nodes. The aggregate installation also exposes both nodes.

Create a private Langflow credential containing an [Ace Data Cloud application API key](https://platform.acedata.cloud/console/applications) with access to `/acemusic/audios` and `/acemusic/tasks`. Bind the credential to both nodes. Enter a musical idea and choose `acemusic-v1.1` or `acemusic-v1`. Generate submits one paid song request. Connect its result to Retrieve Task or paste the original task ID. You can run the retrieve-only example while the task is pending. A partial result keeps delivered media and reports `partial_failed`. [Public contract](https://github.com/AceDataCloud/ACEMusicAPI)
