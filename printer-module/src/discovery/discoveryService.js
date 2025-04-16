// discoveryService.js

// Require de bonjour module in plaats van mdns
const bonjour = require('bonjour')();

class PrinterDiscoveryService {
  constructor() {
    this.discoveredPrinters = [];
    this.browser = null;
  }

  // Hulpfunctie om te controleren of de service waarschijnlijk een Epson printer betreft
  isEpsonPrinter(service) {
    return service.name && service.name.toLowerCase().includes('epson');
  }

  startDiscovery() {
    // Zoek naar services van type 'ipp' (IPv6/IPv4 printing)
    // Pas indien nodig het type aan aan wat jouw printers uitzenden
    this.browser = bonjour.find({ type: 'ipp' }, service => {
      if (this.isEpsonPrinter(service)) {
        // Voeg toe als nog niet aanwezig
        if (!this.discoveredPrinters.find(p => p.name === service.name)) {
          this.discoveredPrinters.push(service);
          console.log(`Printer gevonden: ${service.name} op ${service.addresses[0]}`);
        }
      }
    });

    // Let op: bonjour biedt geen automatisch "serviceDown" event. 
    // Als je later printers wilt verwijderen (als ze offline gaan), kun je extra logica implementeren.
  }

  getPrinters() {
    return this.discoveredPrinters;
  }

  refreshDiscovery() {
    // Stop de huidige discoverysessie (indien beschikbaar) en start opnieuw
    if (this.browser) {
      // Stop de bonjour-browser door de bonjour-instantie te vernietigen
      bonjour.destroy();
    }
    this.discoveredPrinters = [];
    // Herstart de discovery
    this.startDiscovery();
    return this.getPrinters();
  }
}

module.exports = new PrinterDiscoveryService();