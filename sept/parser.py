from sept.token_manager import TokenManager
from sept.operator_manager import OperatorManager
from sept.documentation import DocumentationGenerator
from sept.template import Template


class PathTemplateParser(object):
    def __init__(self, additional_tokens=None, additional_operators=None):
        super(PathTemplateParser, self).__init__()

        self._token_manager = TokenManager()
        if additional_tokens:
            self._token_manager.add_custom_tokens(additional_tokens)

        self._operator_manager = OperatorManager()
        if additional_operators:
            self._operator_manager.add_custom_operators(additional_operators)

        self._documentation_generation = DocumentationGenerator(
            token_manager=self._token_manager,
            operator_manager=self._operator_manager,
        )

    def operator_documentation(self):
        return self._documentation_generation.generate_operator_documentation()

    def token_documentation(self):
        return self._documentation_generation.generate_token_documentation()

    def parse(self, template, data):
        if not isinstance(template, Template):
            template = self.validate_template(template)

        return template.resolve(data)

    def validate_template(self, template_str, default_fallback_token=True):
        template = Template.from_template_str(
            template_str=template_str,
            tmanager=self._token_manager,
            omanager=self._operator_manager,
            default_fallback=default_fallback_token,
        )
        return template
