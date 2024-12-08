from typing import Any, Dict
from http import HTTPStatus
from collections import defaultdict


class ResponsesCreater:
    @classmethod
    def responses_creater(cls, response_list: list[tuple[int, Any]]) -> Dict[Any, Any]:
        group = defaultdict(list)

        for status_code, detail in response_list:
            group[status_code].append(detail)

        responses = {}

        for status_code, details in group.items():
            responses[status_code] = {
                "description": HTTPStatus(status_code).phrase,
                "content": {
                    "application/json": {
                        "examples": cls.make_examples(detail_list=details)
                    }
                },
            }

        return responses

    @classmethod
    def make_examples(cls, detail_list: list[str]) -> dict[str, Any]:
        examples = {}

        for detail in detail_list:
            examples[detail] = {"value": {"detail": detail}}

        return examples
