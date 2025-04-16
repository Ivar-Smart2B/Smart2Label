# Functionele Wensen & Beschrijvingen

Deze lijst bevat alle gewenste functies en ontwerpprincipes die als leidraad dienen voor het bouwen van de SAAS labeldesigner voor Epson ColorWorks printers. Elk onderdeel moet rekening houden met uitbreidbaarheid, gebruiksvriendelijkheid en ondersteuning van ESC/Label zonder printerdriver.

---

## 🔧 Algemene Functionaliteiten
- Directe ESC/Label printoutput zonder tussenkomst van printerdrivers
- SaaS-opbouw met gebruikerslogin en licentiestructuur
- Mogelijkheid om labelontwerpen op te slaan, te dupliceren en later te bewerken
- CSV- en Excel-import voor variabele data zoals tekst, barcodes of nummers
- Werkt op Windows, Mac, iPad en mobiel (responsive)

---

## 🎨 Canvas & Labelinstellingen
- Gebruiker kan handmatig labelafmetingen instellen (breedte x hoogte in mm)
- Instellingen voor:
  - Label spacing
  - Media type (coating)
  - Snij-instellingen (bijv. na elk label snijden)
- Automatisch tonen van printable area op basis van geselecteerde printer
- Opslaan van aangepaste canvasformaten als template

---

## ✏️ Tekstobjecten
- Handmatig tekstblok toevoegen via toolbar
- Instelbare lettertypes, kleuren, groottes, regel- en letterafstand
- Automatische tekstschaal zodat tekst altijd past binnen tekstvak
- Uitlijning: links, midden, rechts, boven, onder, verticaal centreren
- Variabele tekstinhoud via koppeling met CSV/Excel
- Teksttransformaties: hoofdletters, kleine letters, Hoofdletter Eerste Woord
- Mogelijkheid tot samenvoegen van meerdere gegevens in één tekstveld

---

## 📦 Barcodes & QR-Codes
- Ondersteunde types: EAN13, Code128, Interleaved 2/5, QR, DataMatrix
- Instelbare afmetingen, DPI-afhankelijke scherpte
- Validatie van invoer (bijv. correcte lengte voor EAN13)
- Voorvertoning van barcode op ware grootte
- Variabele data mogelijk vanuit externe bron

---

## 🖼️ Afbeeldingen
- Upload mogelijkheid of slepen in canvas
- Schalen, draaien, positioneren
- Ondersteuning voor PNG/JPG
- Optionele automatische achtergrondverwijdering (voor logo’s)
- Toekomst: variabele afbeeldingen per CSV-regel

---

## 🔷 Vormen
- Rechthoeken, lijnen, cirkels en ellipsen
- Instelbare kleuren, transparantie, randdikte
- Handige toepassing voor visuele structuur of branding

---

## 📆 Variabele Gegevens
- Printdatum met offset (bijv. vandaag + 2 dagen)
- Oplopende serienummers (met prefix en/of suffix)
- Geavanceerde regels: bijv. “Toon QR-code alleen als kolom X niet leeg is”

---

## 🔁 Drag & Drop Editor
- Links: gereedschapsbalk (tekst, afbeelding, barcode, vorm)
- Midden: canvas (volledig WYSIWYG)
- Rechts: eigenschappenpaneel dat verandert op basis van geselecteerd object
- Snapping & alignment tools
- Rasterweergave (optioneel in-/uitschakelbaar)

---

## 💾 Projectbeheer
- Labels kunnen worden opgeslagen, hernoemd en gedupliceerd
- Projecten zijn gelinkt aan gebruikersaccounts
- Sjablonen beschikbaar voor hergebruik
- Printgeschiedenis per gebruiker (optioneel activeren)

---

## 🧠 Extra Functionaliteiten
- ESC/Label code preview voor technische gebruikers
- Sneltoetsen voor veelgebruikte acties (D = dupliceren, Del = verwijderen)
- Undo/Redo functionaliteit
- Live preview van labelresultaat op canvas

---

## 📱 Responsive Ontwerp
- Werkt op desktop, tablet en mobiel
- UI schaalt mee, touch drag & drop actief
- Grote knoppen voor bediening op touchscreen