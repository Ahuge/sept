from sept.errors import (
    ClosingBalancingParenthesisError,
    OpeningBalancingParenthesisError,
)

START_TOK = "{"
CLOSE_TOK = "}"


class ParenthesisBalancer(object):
    """
    The ParenthesisBalancer class runs a stack based pairing lookup against the "{{" and "}}" pairs.

    It will check for any unbalanced pairs and return a record of those in addition to any successfuly found pairs

    Successfully matched pairs get returned as a list of [start_index, end_index] values which can be used to generate substrings of only the "Token Expression" chunks.
    """

    def __init__(self, template_str):
        super(ParenthesisBalancer, self).__init__()
        self.template_str = template_str
        self._open_count = 0
        self._root_locations = []
        self._currently_open_locations = []
        self._recently_closed_locations = []
        self._single_opens = []
        self._single_closes = []
        self._errors = []

    def execute(self):
        """
        execute the template parsing.
        This method runs the token balancing check and will store any errors as either `sept.errors.OpeningBalancingParenthesisError` or `sept.errors.ClosingBalancingParenthesisError` exceptions, unthrown.

        It returns any successfully found "Token Expressions" at the root level. Any nested "Token Expressions" get validated but not returned as locations from this method.

        :return: Returns a list of "Token Expression" locations as index start:end values and a list of any errors that were encountered.
        :rtype: list[list,list]
        """
        # msg = " {} ".format(msg)
        for index, curr_char in enumerate(self.template_str):
            prev_char, next_char = self._get_chars(curr_index=index)

            if curr_char == START_TOK:
                self._single_opens.append(index)
            elif curr_char == CLOSE_TOK:
                self._single_closes.append(index)

            if self._is_start_tok(curr_char, next_char):
                # Might have a tok_start
                if prev_char == START_TOK:
                    if index - 2 in self._currently_open_locations:
                        # We have nested goupings
                        self.open_group(curr_index=index)
                    continue
                self.open_group(curr_index=index)

            elif curr_char == CLOSE_TOK:
                if next_char == CLOSE_TOK:
                    # Might have a tok_close
                    if prev_char == CLOSE_TOK:
                        if index - 2 in self._recently_closed_locations:
                            # We are closing a nested grouping
                            self.close_group(curr_index=index)
                        continue
                    self.close_group(curr_index=index)
        if self._currently_open_locations:
            for open_location in self._currently_open_locations:
                next_close = open_location
                for close_index in reversed(self._single_closes):
                    if close_index < open_location:
                        break
                    next_close = close_index
                self._errors.append(
                    ClosingBalancingParenthesisError(
                        start_location=open_location,
                        end_location=next_close,
                        missing_token=CLOSE_TOK + CLOSE_TOK,
                        substr=self.template_str[open_location:],
                    )
                )

        return self._root_locations, self._errors

    def _is_start_tok(self, curr_char, next_char):
        if curr_char == START_TOK:
            if next_char == START_TOK:
                return True
        return False

    def _get_chars(self, curr_index):
        if curr_index == 0:
            prev_char = None
        else:
            prev_char = self.template_str[curr_index - 1]

        if curr_index == len(self.template_str) - 1:
            next_char = None
        else:
            next_char = self.template_str[curr_index + 1]
        return prev_char, next_char

    def open_group(self, curr_index):
        self._open_count += 1
        self._currently_open_locations.append(curr_index)

    def close_group(self, curr_index):
        if self._open_count <= 0:
            last_closed = 0
            if self._recently_closed_locations:
                last_closed = self._recently_closed_locations[-1]

            last_open = last_closed + 2
            for open_index in reversed(self._single_opens):
                if open_index < last_closed:
                    break
                last_open = open_index

            end_index = curr_index + 1
            self._errors.append(
                OpeningBalancingParenthesisError(
                    start_location=last_open,
                    end_location=end_index,
                    missing_token=START_TOK + START_TOK,
                    substr=self.template_str[last_open : end_index + 1],
                )
            )
            return
        self._open_count -= 1
        last_opener = self._currently_open_locations.pop()
        if not self._currently_open_locations:
            self._root_locations.append((last_opener, curr_index + 1))
        self._recently_closed_locations.append(curr_index)

    @classmethod
    def parse_string(cls, template_str):
        """
        Standard entrypoint into usage of the ParenthesisBalancer class

        :param str template_str: Template string that we want to validate.
        :return: Tuple of expression_locations and errors. See `execute` for definition.
        :rtype: list[list,list]
        """
        _b = cls(template_str)
        return _b.execute()
