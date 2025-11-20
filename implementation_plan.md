# Add list_chunks tool

I will add a new tool `list_chunks` to the `dify-ragflow-plugin`. This tool will allow users to list chunks of a specific document in a dataset, with optional keyword filtering and pagination.

## User Review Required

None.

## Proposed Changes

### Tools

#### [NEW] [list_chunks.yaml](file:///e:/code/github/dify-ragflow-plugin/tools/list_chunks.yaml)
- Define the tool metadata and parameters.
- Parameters: `dataset_id`, `document_id`, `page`, `page_size`, `keywords`.

#### [NEW] [list_chunks.py](file:///e:/code/github/dify-ragflow-plugin/tools/list_chunks.py)
- Implement the tool logic using `ragflow_sdk`.
- It will:
    1. Initialize `RAGFlow` client.
    2. Get the dataset by `dataset_id` (I need to find how to get dataset by ID, probably `ragflow.get_dataset(id)` or iterate).
       - Wait, `ragflow.list_datasets` returns datasets. Does it have `get_dataset`?
       - If not, I might have to use `ragflow_api.py` or assume `ragflow.get_dataset(name)`?
       - Actually, `list_datasets` tool uses `ragflow_client.list_datasets`.
       - I'll assume I can get a dataset object. If `get_dataset` exists, great. If not, I might have to list and filter? No, that's inefficient.
       - Let's assume `ragflow.get_dataset(id)` exists or I can construct a `Dataset` object manually if SDK allows.
       - However, usually SDKs allow `client.get_dataset(id)`.
       - Let's search for "ragflow sdk get_dataset".

#### [MODIFY] [provider/ragflow.yaml](file:///e:/code/github/dify-ragflow-plugin/provider/ragflow.yaml)
- Register the new tool.

## Verification Plan

### Automated Tests
- I cannot run automated tests easily without a real RAGFlow instance.
- I will rely on code review and ensuring the code structure matches existing tools.

### Manual Verification
- I will check if the files are created and content looks correct.
