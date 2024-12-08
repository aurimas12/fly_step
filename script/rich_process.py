from rich.table import Table, Column
from typing import List, Dict
from rich.console import Console


def display_chipest_flights_in_table(data: List[Dict[str, str]]) -> None:
    """
    Displays the cheapest flight data in a rich table format.
    Args:
        data(List[Dict[str, str]]):
        data from def prepare_flight_formated_output()
        exp: {'departureDate': '2024-12-13 12:55:00',
            'from': 'Vilnius', 'to': 'Barcelona',
            'direction': 'Vilnius (VNO) -> Barcelona (BCN)',
            'price': 39.99}
        A list of flight dictionaries, where each dictionary includes from
        json_data_process.py def prepare_flight_formated_output():
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
        Column("Price (EUR)", justify="left", style="red"),
        title="Chipest Flight Information",
        title_style = "orange3",
        show_header=True,
        header_style="bold dark_red"
    )

    for item_dict in data:
        departure_date = item_dict['departureDate']
        direction = item_dict['direction']
        price = item_dict['price']
        table.add_row(departure_date, direction, str(price))

    console.print(table)
