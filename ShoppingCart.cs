using System.ComponentModel.DataAnnotations;

namespace Eshop.Models
{
    public class ShoppingCart
    {
        [Key]
        public int CartId { get; set; }
        public List<CartItem>? Items { get; set; }
        public decimal TotalPrice { get; set; }
    }
}
