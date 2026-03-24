# RAGFlow Dify Plugin

**Author:** [leslie2046](https://github.com/leslie2046)
**Version:** 0.0.3
**Type:** Tool
**Repo:** [dify-ragflow-plugin](https://github.com/leslie2046/dify-ragflow-plugin)

## Description
This plugin integrates RAGFlow into Dify, allowing you to manage datasets, documents, chunks, retrieval, and memory workflows from your RAGFlow instance directly inside Dify.

## Tools
The plugin provides the following tools:

- **List Datasets**: List datasets in RAGFlow.
- **List Documents**: List documents within a specific dataset.
- **List Chunks**: List chunks from a document.
- **Retrieve**: Retrieve relevant chunks from RAGFlow based on a query.
- **List Memory**: List memories in RAGFlow.
- **Create Memory**: Create a memory with selected memory types and model IDs.
- **Update Memory**: Update a memory using a JSON object payload.
- **Delete Memory**: Delete a memory by ID.
- **Add Message**: Add a user/agent message pair into one or more memories.
- **Search Messages**: Search memory messages semantically or by keywords.
- **Get Recent Messages**: Retrieve recent messages from one or more memories.
- **List Memory Messages**: List paginated messages inside a specific memory.
- **Get Message Content**: Fetch the stored content for a specific memory message.
- **Update Message Status**: Enable or disable a specific memory message.
- **Forget Message**: Remove a specific message from a memory.

## Configuration
To use this plugin, you need to configure the following credentials:

- **Base URL**: The API base URL of your RAGFlow instance (e.g., `http://<your-ragflow-host>`).
- **API Key**: Your RAGFlow API Key.
