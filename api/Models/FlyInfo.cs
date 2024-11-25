namespace api.Models
{
    public class FlyInfo
    {
        public DateTime DepartureDate { get; set; }
        public DateTime ArrivalDate { get; set; }
        public string? FlightNumber { get; set; }
        public decimal PriceUpdated { get; set; }
        public DepartureAirport? DepartureAirport { get; internal set; }
        public ArrivalAirport? ArrivalAirport { get; internal set; }
        Price? Price { get; set; }
    }
}
