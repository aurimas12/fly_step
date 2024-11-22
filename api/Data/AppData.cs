using Microsoft.EntityFrameworkCore;

namespace api.Data
{
    public class AppData : DbContext
    {
        public AppData(DbContextOptions<AppData> options) :
            base (options) { }
    }
}
