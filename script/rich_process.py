from rich.text import Text
import re
from rich.table import Table, Column
from rich.console import Console
from typing import List, Dict


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


def display_chipest_flights_in_table(data: List[Dict[str, str]]) -> None:
    """
    Displays the cheapest flight data in a rich table format.
    Args:
        data(List[Dict[str, str]]):
        A list of flight dictionaries, where each dictionary includes from
        function prepare_flight_formated_output():
            'departureDate' (str): The departure date and time as a string.
            'direction' (str): The direction in the format 'City (IATA) -> City (IATA)'.
            'price' (str or float): The flight price in euros.
    Returns:
        None: Prints the table of cheapest flights to the console.
    """
    console = Console()
    table = Table(
        Column("Departure Date", justify="center", style="cyan"),
        Column("Direction", justify="left", style="green"),
        Column("Price (€)", justify="left", style="green"),
        title="Chipest Flight Information",
        title_style = "orange3",
        show_header=True,
        header_style="bold dark_red"
    )
    for flight in data:
        departure_date = flight['departureDate']
        direction = flight['direction']
        price = flight['price']
        table.add_row(departure_date, direction, str(price))

    console.print(table)
