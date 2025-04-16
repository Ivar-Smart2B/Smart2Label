# Architectuur & Structuur – Overzicht Projectopzet

## Inleiding

Dit document beschrijft de basisarchitectuur voor onze SAAS-webapplicatie die ESC/Label-printopdrachten genereert voor Epson ColorWorks labelprinters. Door een gelaagde en modulaire architectuur te hanteren, bouwen we een flexibel systeem dat uitbreidbaar, schaalbaar en goed testbaar is gedurende alle ontwikkelfasen.

## 1. Doelstellingen

- **Modulariteit:** Scheid de functionaliteiten zodat nieuwe modules (bijv. voor variabelenbeheer, authenticatie of printer integratie) onafhankelijk kunnen worden ontwikkeld en getest.
- **Flexibiliteit:** Door losse koppelingen tussen lagen kunnen toekomstige wijzigingen in gebruikersinterface, business logica of infrastructuur zonder ingrijpende herstructurering doorgevoerd worden.
- **Testbaarheid & Onderhoudbaarheid:** Elke laag is verantwoordelijk voor een specifieke set functies, waardoor unit- en integratietests eenvoudiger worden en het onderhoud overzichtelijk blijft.
- **Integratie van ESC/Label:** Het aansturen van Epson ColorWorks printers via ESC/Label commando’s wordt in een aparte printermodule afgehandeld, zodat wijzigingen in de commando-specificaties geïsoleerd blijven.

## 2. Gelaagde Architectuur

We hanteren een Clean Architecture waarbij de applicatie is verdeeld in vier hoofdlagen:

### 2.1 Presentatielaag (Frontend)

- **Technologieën:** 
  - Een moderne Single Page Application (SPA) gebouwd met React.
  - Integratie van grafische bibliotheken zoals Konva.js of Fabric.js voor een interactieve canvas-editor met drag & drop functionaliteit.
- **Doel:** Zorgt voor een responsieve en intuïtieve gebruikersinterface die op alle devices (Windows, Mac, iPad en mobiel) optimaal werkt.
- **Communicatie:** Verbindt met de backend via RESTful API’s of GraphQL, zodat de presentatie volledig losgekoppeld is van de business logica.

### 2.2 Applicatielaag (Business Logica)

- **Modulaire opzet:** Bevat de kernlogica voor labelontwerp en -bewerking, validatie van invoer, en de mapping van de ontwerpdata naar ESC/Label commando’s.
- **Belangrijke modules:**
  - **ESC/Label Generator:** Vertaling van domeinobjecten (zoals tekst, barcodes, afbeeldingen) naar nauwkeurige commando’s voor de printer (volgens de ESC/Label specificaties).
  - **Printcontroller:** Verantwoordelijk voor de dispatching en verwerking van printopdrachten, inclusief foutafhandeling en statusbeheer.
  - **Projectbeheer en Authenticatie:** Modules voor gebruikersbeheer, sjabloonbeheer en licentiecontrole.
- **Voordeel:** Veranderingen in business regels en logica kunnen onafhankelijk van de frontend worden doorgevoerd.

### 2.3 Domeinlaag (Core Domain)

- **Kernconcepten:** Definieert de entiteiten en objecten zoals labels, tekstobjecten, barcodes, afbeeldingen en hun onderlinge relaties.
- **Logica & Validatie:** Bevat alle domeinspecifieke validatieregels (bijvoorbeeld invoervereisten voor barcodes, samenvoegen van variabele data) en business logica.
- **Voordeel:** Houdt de “zuivere” bedrijfsregels los van technologie en infrastructuur, wat het systeem robuust en herbruikbaar maakt.

### 2.4 Infrastructuurlaag

- **Data Opslag:** Gebruik van een relationele database (bijvoorbeeld PostgreSQL) voor het opslaan van gebruikersdata, projecten en ontwerpen.
- **Externe Integraties:**
  - **Printer integratie:** Een volledig gecapsuleerde module voor het aansturen van printers middels ESC/Label commando’s.
  - **Authenticatie en licentiebeheer:** Integratie met eventueel externe Identity Providers.
- **Repository Pattern:** Door een duidelijke scheiding in data-access op te zetten, kunnen de business logic en domeinlaag onafhankelijk blijven van de gekozen opslagtechnologie.

## 3. Communicatie & Integratie

- **API-laag:** Een robuuste API-gateway die zorgt voor een losgekoppelde communicatie tussen frontend en backend.
- **Printermodule:** Een specifieke component die de ESC/Label commando’s genereert en direct naar de printer stuurt. Deze module verwerkt alle variaties voor diverse printerseries (zoals CW-C4000, CW-C8000, etc.) op een centrale en geïsoleerde wijze.

## 4. Voordelen van de Geadviseerde Architectuur

- **Losse koppeling:** Wijzigingen in een laag (bijv. de user interface) hebben minimale impact op andere lagen.
- **Schaalbaarheid:** Nieuwe functionaliteiten kunnen eenvoudig worden toegevoegd als afzonderlijke modules zonder de bestaande architectuur te breken.
- **Onderhoud & Testbaarheid:** Elke laag kan afzonderlijk worden getest, wat de kans op fouten verkleint en het onderhoud vereenvoudigt.
- **Toekomstbestendigheid:** De modulariteit en duidelijke scheiding van verantwoordelijkheden maken het systeem flexibel voor toekomstige uitbreidingen of wijzigingen in de printercommando’s.

## 5. Conclusie & Actiepunten

Deze gelaagde en modulaire architectuur vormt de solide basis voor ons project. Het biedt een duidelijk kader waarbinnen we tijdens alle ontwikkelfasen (Fase 1 tot Fase 5) gemakkelijk kunnen uitbreiden, wijzigen en testen.

**Actiepunten:**
- **Basisprojectstructuur opzetten:** De mappenstructuur (zoals beschreven in het document) implementeren in de repository.
- **Kernmodellen definiëren:** Het vastleggen van domeinmodellen en interfaces.
- **Prototypes uitwerken:** Eerste prototypes voor de ESC/Label Generator en de Canvas Editor bouwen.
- **API-laag implementeren:** Zorgdragen voor een gestroomlijnde communicatie tussen de frontend en backend.
- **Printermodule opzetten:** Voor het koppelen en aansturen van de printer via ESC/Label commando’s.

---

Dit bestand dient als leidraad gedurende het hele project en helpt ons om consistent te blijven in onze ontwikkeling.

