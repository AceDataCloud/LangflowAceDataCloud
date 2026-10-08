# Privacy

The `lfx-acedatacloud` extension runs inside your Langflow process. It sends the selected prompt, query, media URL or task ID to `https://api.acedata.cloud` with your Ace Data Cloud application API key. The chat provider uses Ace Data Cloud's OpenAI-compatible endpoint. The extension does not call another host or collect its own analytics.

Store the key as a Langflow **Credential** global variable. Langflow manages that value in its credential store; this package does not write a separate key file. A flow export can contain a literal key if you choose to put one into a field, so inspect exports before sharing them. The supplied examples contain no key. Do not include keys in support requests.

Service results may contain generated-media URLs. Anyone who obtains an accessible URL may be able to open the media. Review inputs and outputs before publishing a flow or sharing a trace.

Ace Data Cloud account, API usage, and data handling follow the [Ace Data Cloud site terms and privacy policy](https://platform.acedata.cloud). For package questions, use [GitHub Issues](https://github.com/AceDataCloud/LangflowAceDataCloud/issues) or dev@acedata.cloud.
