# 在 Langflow 中使用 Suno by Ace Data Cloud

这是Ace提供的Suno集成，不是原服务官方插件。独立的Generate和Retrieve Task节点支持一次生成、同ID查询。英文版见[Suno guide](suno.md)。

## 1. 安装并找到节点

在运行 Langflow 的同一 Python 环境安装后重启：

```bash
python -m pip install "lfx-acedatacloud-suno==0.1.3"
```

[v0.1.3 GitHub Release](https://github.com/AceDataCloud/LangflowAceDataCloud/releases/tag/v0.1.3) 也提供该服务的独立 wheel。打开 **Components → Suno by Ace Data Cloud**，或直接搜索服务名。单服务包只注册两个节点，不注册聊天 Provider。使用该 Python 包内 `examples/` 的生成/纯查询两份无 Key 流程；详见[包 README](../packages/suno/README.md)。

[合集安装](../README_zh_CN.md#1-安装扩展)提供全部服务和原生聊天 Provider。根目录[生成示例](../examples/suno.json)及[纯查询示例](../examples/retrieve_only/suno.json)使用合集 ID；独立包的示例使用单服务 ID，两种分类可以共存，不替换旧保存节点。[官方默认收录](https://github.com/langflow-ai/langflow/pull/15659)仍在审核，拟发布官方文档 URL 在获接受前可能不可用。

## 2. 注册、取得应用API Token

打开[Ace Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_suno_guide_api_key)注册或登录。无通用应用时先点**Initialize General Application**。复制General application的API Key，或**Manage Keys → Create**创建专用Langflow Key。先核Suno服务权限、有效期、调用限额、[当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_suno_guide_pricing)和余额。若限制Allowed APIs，至少允许`/suno/audios`和`/suno/tasks`。

只复制原始token，不加`Bearer `或引号，不用账号管理token。以下为Ace既有真实控制台截图（2026-10-12源版本），敏感Key已打码。

![复制应用Key或管理密钥](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![创建可限制权限的专用Key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

## 3. 在Langflow粘贴位置

**Settings → Global Variables → Add New**，Type选**Credential**，Name填`ACEDATACLOUD_API_KEY`，Value粘贴token并保存。在Generate和Retrieve Task两个节点的**Ace Data Cloud API key**右侧地球图标中选择此变量。不要把真实Key放到提示词或导出的JSON。

![尚未填Key的真实Langflow凭据窗口](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/59beda518889ff106f64da9caaad56e59690a6e4/_assets/tutorial/17-create-credential.png)

这是2026-10-09、Langflow1.12.5历史截图，不是新Suno调用证明；后续版本位置可能变化。

## 4. 一次生成，查询原任务

连接**Suno Generate → Suno Retrieve Task → Chat Output**。将Generate结果连到Retrieve Task的**Submitted task**。现有示例字段如下；模型与价格可能变化，运行前重新核对，不擅换模型。

| 字段 | 首用值 |
| --- | --- |
| Prompt (`prompt`) | `A short gentle instrumental piano melody for a sunrise, no vocals.` |
| Model (`model`) | `chirp-v6` |
| Instrumental (`instrumental`) | `True` |
| Target duration (seconds) (`duration`) | `10` |
| Additional route parameters | `{"async": true}` |
| Wait up to seconds | `240` |

精确提示词和字段见[示例JSON](../examples/suno.json)。只点击一次Chat Output运行按钮。生成是收费提交，查询是同一任务；`pending`不是完成，绿色节点或预览也不代表媒体成功。

![真实Langflow连接方式参考：GPT Image示例](https://raw.githubusercontent.com/AceDataCloud/LangflowAceDataCloud/59beda518889ff106f64da9caaad56e59690a6e4/_assets/tutorial/13-imported-gpt-image-flow.png)

这是2026-10-09的GPT Image流程配置原图，只说明通用连线，不冒充新Suno流程运行或官方内置证明。

若等待结束仍pending，导入[只查询流程](../examples/retrieve_only/suno.json)，填原task ID并绑定同一凭据。不要重新点Generate轮询。若提交超时，先查Usage History找回原task/trace，再决定是否另发；不能因不知道状态重复扣费。

终态输出应有`status=succeeded`、`success=true`和`media_urls`。打开返回的媒体链接，再到[Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=langflow_suno_guide_usage)按原task/trace核对一条账单。Credits不是USD，历史测试价格不保证将来价格。

## 常见问题

- 搜不到：核同一Python环境安装并重启；确认已安装0.1.3或以上版本。
- 401/403：核原始应用token、服务权限、余额和提交/查询接口白名单。
- 400：核当前模型及该路由参数。
- 429：降低并发，保持自动收费重试关闭。
- pending/超时：只查原任务；不要为查进度再生成。

[能力矩阵](../CAPABILITIES_zh_CN.md)保留各服务测试等级。扩展免费，API调用按当前价格收费；未宣称覆盖全部高级动作或所有UI路径。
