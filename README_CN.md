# RAGFlow Dify 插件

**Author:** [leslie2046](https://github.com/leslie2046)
**Version:** 0.0.3
**Type:** Tool
**Repo:** [dify-ragflow-plugin](https://github.com/leslie2046/dify-ragflow-plugin)

## 描述
本插件将 RAGFlow 集成到 Dify 中，允许您直接在 Dify 工作流中管理 RAGFlow 实例中的数据集、文档、块、检索和记忆能力。

## 工具
本插件提供以下工具：

- **List Datasets (列出数据集)**: 列出 RAGFlow 中的数据集。
- **List Documents (列出文档)**: 列出特定数据集中的文档。
- **List Chunks (列出块)**: 列出文档中的块。
- **Retrieve (检索)**: 根据查询从 RAGFlow 检索相关块。
- **List Memory (列出记忆)**: 列出 RAGFlow 中的记忆。
- **Create Memory (创建记忆)**: 使用指定的记忆类型和模型 ID 创建记忆。
- **Update Memory (更新记忆)**: 使用 JSON 对象载荷更新记忆。
- **Delete Memory (删除记忆)**: 根据 ID 删除记忆。
- **Add Message (添加消息)**: 向一个或多个记忆写入一组用户/助手消息。
- **Search Messages (搜索消息)**: 对记忆消息执行语义或关键词搜索。
- **Get Recent Messages (获取最近消息)**: 获取一个或多个记忆中的最近消息。
- **List Memory Messages (列出记忆消息)**: 分页列出某个记忆中的消息。
- **Get Message Content (获取消息内容)**: 获取某条记忆消息的存储内容。
- **Update Message Status (更新消息状态)**: 启用或禁用某条记忆消息。
- **Forget Message (忘记消息)**: 从记忆中删除指定消息。

## 配置
要使用此插件，您需要配置以下凭据：

- **Base URL**: 您的 RAGFlow 实例的 API 基础 URL (例如 `http://<your-ragflow-host>`)。
- **API Key**: 您的 RAGFlow API 密钥。
