using api.Models;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class FlightsController : ControllerBase
{
    private static readonly List<FlyInfo> Flights = new()
    {
        new FlyInfo
        {
            DepartureDate = new DateTime(2024, 11, 26, 10, 30, 0),
            ArrivalDate = new DateTime(2024, 11, 26, 14, 45, 0),
            FlightNumber = "AB123",
            DepartureAirport = new DepartureAirport { DataCode = "VNO", Name = "Vilnius Airport", CountryName = "Vilnius" },
            ArrivalAirport = new ArrivalAirport { DataCode = "LHR", Name = "London Heathrow", CountryName = "London" }
        },
        new FlyInfo
        {
            DepartureDate = new DateTime(2024, 11, 27, 12, 00, 0),
            ArrivalDate = new DateTime(2024, 11, 27, 15, 30, 0),
            FlightNumber = "XY456",
            DepartureAirport = new DepartureAirport { DataCode = "KUN", Name = "Kaunas Airport", CountryName = "Kaunas"},
            ArrivalAirport = new ArrivalAirport { DataCode = "RIX", Name = "Riga Airport", CountryName = "Riga" }
        }
    };

    [HttpGet]
    public IActionResult GetFlights(string? departureData, string? arrivalData, DateTime? departureDate)
    {
        var filteredFlights = Flights.Where(f =>
            (string.IsNullOrEmpty(departureData) || f.DepartureAirport.DataCode == departureData) &&
            (string.IsNullOrEmpty(arrivalData) || f.ArrivalAirport.DataCode == arrivalData) &&
            (!departureDate.HasValue || f.DepartureDate.Date == departureDate.Value.Date)
        ).ToList();

        return Ok(filteredFlights);
    }
}
