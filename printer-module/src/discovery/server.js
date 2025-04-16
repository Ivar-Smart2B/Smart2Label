// server.js

const express = require('express');
const discoveryService = require('./discoveryService');

const app = express();
const port = 3000;

// Start de printer discovery wanneer de server opstart
discoveryService.startDiscovery();

// Endpoint om de huidige printers op te halen
app.get('/printers', (req, res) => {
  res.json(discoveryService.getPrinters());
});

// Endpoint om de discovery te verversen
app.post('/printers/refresh', (req, res) => {
  const updatedList = discoveryService.refreshDiscovery();
  res.json(updatedList);
});

app.listen(port, () => {
  console.log(`Printer Discovery API draait op http://localhost:${port}`);
});
