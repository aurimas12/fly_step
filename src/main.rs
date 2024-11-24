use slint::{SharedString, Weak};

slint::include_modules!();

fn main() -> Result<(), slint::PlatformError> {
    let ui:AppWindow = AppWindow::new()?;
    let ui_handle:Weak<AppWindow>=ui.as_weak();
    ui.on_cheapest_fly(move | departure_from:SharedString, departure_to:SharedString, fly_date:SharedString|{
        println!("From: {}, To: {}, Date: {}", departure_from, departure_to, fly_date);
        let ui=ui_handle.upgrade().unwrap();
    /*
    
        Ticket api logic
    
     */
    });

    ui.run()
}
