using System.ComponentModel.DataAnnotations;

namespace Eshop.Models
{
    public class CartItem
    {
        [Key]
        public int ItemId { get; set; }
        Product? Product { get; set; }
        public int Quantity { get; set; }
        public decimal Subtotal { get; set; }

    }
}
