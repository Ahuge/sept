from path_template.token_manager import TokenManager
from path_template.operator_manager import OperatorManager
from path_template.template import Template


class PathTemplateParser(object):
    def __init__(self, additional_tokens=None, additional_operators=None):
        super(PathTemplateParser, self).__init__()

        self._token_manager = TokenManager()
        self._token_manager.add_custom_tokens(additional_tokens)

        self._operator_manager = OperatorManager()
        self._operator_manager.add_custom_operators(additional_operators)

    def parse(self, template, data):
        if not isinstance(template, Template):
            template = self.validate_template(template)

        return template.resolve(data)

    def validate_template(self, template_str):
        template = Template.from_template_str(
            template_str=template_str,
            tmanager=self._token_manager,
            omanager=self._operator_manager
        )
        return template
