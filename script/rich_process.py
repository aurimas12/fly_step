from rich.table import Table, Column
from typing import List, Dict
from rich.console import Console


def display_chipest_flights_in_table(data: List[Dict]) -> List[Dict]:
    """
    Displays the cheapest flight_dict data in a rich table format.
    from function prepare_flight_formated_output()
    Args:
        data(List[Dict[str, str]]):
        A list of flight_dict dictionaries, where each dictionary includes from
        def prepare_flight_formated_output():
            'departureDate' (str): The departure date and time as a string.
            'direction' (str): The direction in the format 'City (IATA) -> City (IATA)'.
            'price' (str or float): The flight_dict price in euros.
            exp: {
                'departureDate': '2024-12-13 12:55:00',
                'from': 'Vilnius', 'to': 'Barcelona',
                'direction': 'Vilnius (VNO) -> Barcelona (BCN)',
                'price': 39.99
            }
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
    for flight_dict in data:
        departure_date = flight_dict['departureDate']
        direction = flight_dict['direction']
        price = flight_dict['price']
        table.add_row(departure_date, direction, str(price))

    console.print(table)
