# Langflow 中的 ACE Music

在含有本组件的仓库根目录，从 Langflow 的 Python 环境运行 `python -m pip install ./packages/acemusic`，再重启并搜索 **ACE Music**。新增的两个节点支持根据创意生成歌曲和按原任务号查询。

在 Langflow 中创建私有凭据，填入有 `/acemusic/audios` 和 `/acemusic/tasks` 权限的[应用 API Key](https://platform.acedata.cloud/console/applications)，并绑定到两个节点。输入创意，选择 `acemusic-v1.1` 或 `acemusic-v1`，运行一次生成。把输出连接到查询节点，也可使用单独查询示例粘贴原任务号。部分失败的状态为 `partial_failed`，可使用已交付的单曲。[接口文档](https://github.com/AceDataCloud/ACEMusicAPI)
