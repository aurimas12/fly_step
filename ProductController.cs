using Eshop.Data;
using Eshop.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Eshop.Controllers
{
    public class ProductController : Controller
    {

        private readonly AppDbContext _context;
        public ProductController (AppDbContext context)
        {
            _context = context;
        }

        [HttpGet("GetProductsAsync")]
        public async Task<IEnumerable<Product>> GetProductsAsync()
        {
            return await _context.Products.ToListAsync();
        }
    }
}
