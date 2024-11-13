namespace api.Models
{
    public class City
    {
        public string? Name { get; set; }
        public string? Code { get; set; }
        public string? CountryCode { get; set; }
        DepartureAirport? DepartureAirport { get; set; }
        ArrivalAirport? ArrivalAirport { get; set; }
    }
}
