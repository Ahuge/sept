import pytest

from sept.parser import PathTemplateParser

state_data = {
    "name": "AhUgHeS",
    "first_name": "Alex",
    "last_name": "Hughes",
    "data_with_space": "This is a sentence",
    "deep": {
        "nested": {
            "data": {
                "githubUsername": "Ahuge",
            }
        }
    },
}
parser = PathTemplateParser()


def test_lower():
    template_str = r"{{lower:name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes"


def test_upper():
    template_str = r"{{upper:name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "AHUGHES"


def test_replace():
    template_str = r"{{replace[AhUgHeS,Bobby]: name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "Bobby"


def test_substr():
    template_str = r"{{substr[0,2]:name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "Ah"


def test_substr_keyword_start():
    template_str = r"{{substr[start,2]:name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "Ah"


def test_substr_keyword_end():
    template_str = r"{{substr[1,end]:name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "hUgHeS"


def test_null_operator():
    template_str = r"{{name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "AhUgHeS"


def test_replace_keyword_space():
    template_str = r"{{replace[\s,-]: data_with_space}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "This-is-a-sentence"


def test_lower_substr_nested():
    template_str = r"{{lower:{{substr[1,end]:name}}}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "hughes"


def test_add_custom_operator():
    from sept import Operator

    class SoupOperator(Operator):
        name = "soup"

        def is_invalid(self, token_value):
            return None

        def execute(self, input_data):
            return "tomato soup"

    template_str = r"{{soup:name}}"
    custom_parser = PathTemplateParser(additional_operators=[SoupOperator])
    template_obj = custom_parser.validate_template(
        template_str, default_fallback_token=True
    )

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "tomato soup"


def test_add_custom_token():
    from sept import Token

    class GithubUsernameToken(Token):
        name = "githubusername"

        def getValue(self, data):
            return (
                data.get("deep", {}).get("nested", {}).get("data").get("githubUsername")
            )

    template_str = r"{{lower:githubUsername}}"
    custom_parser = PathTemplateParser(additional_tokens=[GithubUsernameToken])
    template_obj = custom_parser.validate_template(
        template_str, default_fallback_token=True
    )

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahuge"


def test_add_custom_token_with_casing():
    from sept import Token

    class GithubUsernameToken(Token):
        name = "githubUsername"

        def getValue(self, data):
            return (
                data.get("deep", {}).get("nested", {}).get("data").get("githubUsername")
            )

    template_str = r"{{lower:githubUsername}}"
    custom_parser = PathTemplateParser(additional_tokens=[GithubUsernameToken])
    template_obj = custom_parser.validate_template(
        template_str, default_fallback_token=True
    )

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahuge"


def test_incorrect_token_name_casing():
    template_str = r"{{lower:Name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes"


def test_token_length_subset():
    template_str = r"{{lower:name}}/{{upper:name}}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes/AHUGHES"


def test_incorrect_token_name_spacing():
    template_str = r"{{lower: name   }}"
    template_obj = parser.validate_template(template_str, default_fallback_token=True)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes"


if __name__ == "__main__":
    pytest.main()
