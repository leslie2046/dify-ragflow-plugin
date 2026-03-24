import unittest

from memory_tools import (
    ensure_list,
    memory_to_json,
    normalize_result,
    parse_json_object,
    require_list,
    require_string,
    require_memory,
)


class FakeObject:
    def __init__(self, payload):
        self.payload = payload

    def to_json(self):
        return self.payload


class FakeMemory:
    def __init__(self, memory_id, name):
        self.id = memory_id
        self.name = name
        self.memory_type = ["raw"]


class MemoryHelpersTestCase(unittest.TestCase):
    def test_ensure_list_splits_comma_separated_strings(self):
        self.assertEqual(ensure_list("a, b ,c"), ["a", "b", "c"])

    def test_normalize_result_uses_to_json_when_available(self):
        self.assertEqual(normalize_result(FakeObject({"id": "obj-1"})), {"id": "obj-1"})

    def test_normalize_result_recurses_nested_collections(self):
        payload = normalize_result({"items": [FakeObject({"id": "obj-1"}), True]})
        self.assertEqual(payload, {"items": [{"id": "obj-1"}, True]})

    def test_memory_to_json_keeps_known_attributes_json_friendly(self):
        memory = FakeMemory("mem-1", "primary")
        self.assertEqual(
            memory_to_json(memory),
            {"id": "mem-1", "name": "primary", "memory_type": ["raw"]},
        )

    def test_require_memory_returns_matching_memory(self):
        memories = [FakeMemory("mem-1", "primary"), FakeMemory("mem-2", "backup")]
        self.assertIs(require_memory(memories, "mem-2"), memories[1])

    def test_require_memory_raises_when_memory_missing(self):
        with self.assertRaisesRegex(ValueError, "Memory with ID mem-9 not found"):
            require_memory([FakeMemory("mem-1", "primary")], "mem-9")

    def test_parse_json_object_returns_dict(self):
        self.assertEqual(parse_json_object('{"name": "updated"}', "update_json"), {"name": "updated"})

    def test_parse_json_object_rejects_non_object_payloads(self):
        with self.assertRaisesRegex(ValueError, "update_json must be a JSON object"):
            parse_json_object('["not", "an", "object"]', "update_json")

    def test_require_string_returns_string_value(self):
        self.assertEqual(require_string("mem-1", "memory_id"), "mem-1")

    def test_require_string_rejects_missing_values(self):
        with self.assertRaisesRegex(ValueError, "memory_id is required"):
            require_string(None, "memory_id")

    def test_require_list_returns_non_empty_list(self):
        self.assertEqual(require_list("mem-1,mem-2", "memory_id"), ["mem-1", "mem-2"])

    def test_require_list_rejects_empty_values(self):
        with self.assertRaisesRegex(ValueError, "memory_id is required"):
            require_list("  ", "memory_id")


if __name__ == "__main__":
    unittest.main()
