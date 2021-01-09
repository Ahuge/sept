import pytest

from sept.parser import PathTemplateParser
from sept.balancer import ParenthesisBalancer
from sept.errors import (
    ParsingError,
    OperatorNotFoundError,
    OpeningBalancingParenthesisError,
    ClosingBalancingParenthesisError,
    MultipleBalancingError,
)

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
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes"


def test_upper():
    template_str = r"{{upper:name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "AHUGHES"


def test_replace():
    template_str = r"{{replace[AhUgHeS,Bobby]: name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "Bobby"


def test_substr():
    template_str = r"{{substr[0,2]:name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "Ah"


def test_substr_keyword_start():
    template_str = r"{{substr[start,2]:name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "Ah"


def test_substr_keyword_end():
    template_str = r"{{substr[1,end]:name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "hUgHeS"


def test_null_operator():
    template_str = r"{{name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "AhUgHeS"


def test_replace_keyword_space():
    template_str = r"{{replace[\s,-]: data_with_space}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "This-is-a-sentence"


def test_lower_substr_nested():
    template_str = r"{{lower:{{substr[1,end]:name}}}}"
    template_obj = parser.validate_template(template_str)

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
        template_str
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
        template_str
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
        template_str
    )

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahuge"


def test_incorrect_token_name_casing():
    template_str = r"{{lower:Name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes"


def test_token_length_subset():
    template_str = r"{{lower:name}}/{{upper:name}}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes/AHUGHES"


def test_incorrect_token_name_spacing():
    template_str = r"{{lower: name   }}"
    template_obj = parser.validate_template(template_str)

    resolved_path = template_obj.resolve(state_data)
    assert resolved_path == "ahughes"


def test_bad_parsing_error():
    template_str = r"{{lower:name}"
    try:
        parser.validate_template(template_str)
    except ParsingError as err:
        assert err.message == 'Error: Missing closing "}}" characters for Token Expression "{{lower:name}" (0-12)'
    else:
        raise AssertionError("Should have raised a ParsingError!")


def test_bad_parsing_error_multi_expression():
    template_str = r"{{lower:name}}{{upper:name}"
    try:
        parser.validate_template(template_str)
    except ParsingError as err:
        assert err.message == 'Error: Missing closing "}}" characters for Token Expression "{{upper:name}" (14-26)'
    else:
        raise AssertionError("Should have raised a ParsingError!")


def test_bad_parsing_error_multi_expression_start():
    template_str = r"{{lower:name}{{upper:name}}"
    try:
        parser.validate_template(template_str)
    except ParsingError as err:
        assert err.message == 'Error: Missing closing "}}" characters for Token Expression "{{lower:name}{{upper:name}}" (0-26)'
    else:
        raise AssertionError("Should have raised a ParsingError!")


def test_balencer_basic():
    template_str = r"{{lower:name}}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert errors == []
    assert len(token_expresion_locations) == 1
    assert token_expresion_locations[0] == (0, len(template_str)-1)


def test_balencer_double():
    template_str = r"{{lower:name}}{{lower:name}}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert errors == []
    assert len(token_expresion_locations) == 2
    assert token_expresion_locations[0] == (0, 13)
    assert token_expresion_locations[1] == (14, len(template_str)-1)


def test_balencer_double_leading():
    template_str = r"This is a {{lower:name}}{{lower:name}}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert errors == []
    assert len(token_expresion_locations) == 2
    assert token_expresion_locations[0] == (10, 23)
    assert token_expresion_locations[1] == (24, len(template_str)-1)


def test_balencer_basic_missing_opener():
    template_str = r"{lower:name}}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert len(errors) == 1
    assert isinstance(errors[0], OpeningBalancingParenthesisError)
    assert len(token_expresion_locations) == 0


def test_balencer_double_missing_closer():
    template_str = r"{{lower:name}}{lower:name}}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert len(errors) == 1
    assert isinstance(errors[0], OpeningBalancingParenthesisError)
    assert len(token_expresion_locations) == 1
    assert token_expresion_locations[0] == (0, 13)


def test_balencer_basic_missing_closer():
    template_str = r"{{lower:name}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert len(errors) == 1
    assert isinstance(errors[0], ClosingBalancingParenthesisError)
    assert len(token_expresion_locations) == 0


def test_balencer_double_missing_closer():
    template_str = r"{{lower:name}}{{lower:name}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert len(errors) == 1
    assert isinstance(errors[0], ClosingBalancingParenthesisError)
    assert len(token_expresion_locations) == 1
    assert token_expresion_locations[0] == (0, 13)


def test_balencer_double_missing_closer_and_opener():
    template_str = r"{lower:name}}{{lower:name}"
    token_expresion_locations, errors = ParenthesisBalancer.parse_string(
        template_str
    )
    assert len(errors) == 2
    assert isinstance(errors[0], OpeningBalancingParenthesisError)
    assert isinstance(errors[1], ClosingBalancingParenthesisError)
    assert len(token_expresion_locations) == 0


def test_parse_partial_expression():
    template_str = r"{lower:name}}/{{upper:name}}"
    try:
        _ = parser.validate_template(template_str)
    except MultipleBalancingError:
        return True
    else:
        raise AssertionError("Should have raised an OpeningBalancingParenthesisError!")


def test_parse_raise_missing_operator():
    template_str = r"{{lowerr:name}}/{{upper:name}}"
    try:
        _ = parser.validate_template(template_str)
    except OperatorNotFoundError as err:
        return True
    else:
        raise AssertionError("Should have raised a OperatorNotFoundError!")


if __name__ == "__main__":
    pytest.main()
