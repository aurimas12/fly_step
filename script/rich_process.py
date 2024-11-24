from rich.text import Text
import re


def style_numbers_result(result: str) -> Text:
    """
    Styles a result string by highlighting numbers, (numbers, style='red')
    Args:
        result (str): The result string to be styled.
    Returns:
        Text: The styled result with numbers highlighted.
    """
    styled_result = Text()
    for part in re.split(r'(\d+\.\d+|\d+)', result):
        if re.match(r'^\d+\.\d+|\d+$', part):
            styled_result.append(part, style="red")
        else:
            styled_result.append(part)
    return styled_result
