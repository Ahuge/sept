

class DocumentationGenerator(object):
    _overall_operator_html_template = """
    <h1>Operator Documentation</h1>
    <br>
    {operators}
    """
    _operator_divider = "<hr><br>"
    _operator_args_html_template = """<h4>&emsp;<code>Operator Inputs</code></h4>
    {args}
    """
    _operator_arg_html_template = """<h5>
    &emsp;&emsp;<u>{name}</u>: {description}
    <br>&emsp;&emsp;&emsp;&emsp;<code>Required: {required}</code>
    </h5>"""
    _individual_operator_html_template = """
    <h2><code>{name}</code> Operator</h2>
    {operator_args}
    <br>{operator_doc}"""

    def __init__(self, token_manager, operator_manager):
        super(DocumentationGenerator, self).__init__()
        self.token_manager = token_manager
        self.operator_manager = operator_manager

    def generate_operator_documentation(self, operator_manager=None):
        operator_manager = operator_manager or self.operator_manager

        template = self._overall_operator_html_template
        operators_text = []
        for operator in operator_manager.operators:
            operator_args = []
            for arg in operator.args:
                arg_name = arg.get("name", "unnamed")
                arg_description = arg.get("description", "")
                arg_required = arg.get("required", False)
                arg_text = self._operator_arg_html_template.format(
                    name=arg_name,
                    description=arg_description,
                    required=arg_required,
                )
                operator_args.append(arg_text)
            operator_args_text = ""
            if operator_args:
                operator_args_text = self._operator_args_html_template.format(
                    args="".join(operator_args)
                )

            operator_text = self._individual_operator_html_template.format(
                name=operator.name,
                operator_args=operator_args_text,
                operator_doc=operator.__doc__,
            )
            operators_text.append(operator_text)
        return template.format(
            operators=self._operator_divider.join(operators_text)
        )
