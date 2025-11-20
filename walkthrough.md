# Walkthrough - Add list_chunks tool

I have added a new tool `list_chunks` to the `dify-ragflow-plugin`.

## Changes

### Tools

#### [NEW] [list_chunks.yaml](file:///e:/code/github/dify-ragflow-plugin/tools/list_chunks.yaml)
Defined the `list_chunks` tool with parameters:
- `dataset_id`: ID of the dataset.
- `document_id`: ID of the document.
- `page`: Page number (default 1).
- `page_size`: Page size (default 30).
- `keywords`: Optional keywords for filtering.

#### [NEW] [list_chunks.py](file:///e:/code/github/dify-ragflow-plugin/tools/list_chunks.py)
Implemented the tool logic:
1. Initializes `RAGFlow` client.
2. Finds the dataset by iterating through `list_datasets`.
3. Finds the document by iterating through `list_documents`.
4. Calls `document.list_chunks` to retrieve chunks.
5. Yields chunks as JSON.

### Provider

#### [MODIFY] [provider/ragflow.yaml](file:///e:/code/github/dify-ragflow-plugin/provider/ragflow.yaml)
Registered `tools/list_chunks.yaml`.

## Verification Results

### Manual Verification
- Verified that the files exist and syntax looks correct.
- Verified that the tool is registered in `provider/ragflow.yaml`.
