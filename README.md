# 400km Drón Teszt — HF Rádiókommunikációs Szimulátor

**Nagy hatótávolságú (400 km) drón kommunikációs szimulátor, amely HF (High Frequency) rádiócsatornát modellez 2-5 MHz tartományban, telemetria protokollal és zavarásszűréssel (jamming).**

## 📡 Leírás

Ez a szimulátor egy 400 km távolságban működő drón földi állomással folytatott kommunikációját modellezi:

- **HF rádiócsatorna** — 2, 3, 4, 5 MHz frekvenciákon
- **Valós idejű szimuláció** — 5 másodperces kommunikációs ciklusok
- **Jamming szimuláció** — zavarás kapcsolása egyes frekvenciákon
- **Telemetria protokoll** — strukturált adatcsomagok küldése
- **Interaktív irányítás** — billentyűzetről vezérelhető (jamming ki/be)

### Fő komponensek

| Komponens | Fájl | Leírás |
|-----------|------|--------|
| Drón | `drone.py` | A drón oldali adó-vevő és telemetria küldő |
| Földi állomás | `ground_station.py` | Földi vevő és parancsküldő |
| Rádiócsatorna | `radio_channel.py` | HF csatorna modell fadinggel és zajjal |
| Protokoll | `telemetry_protocol.py` | Csomagformátum és adatstruktúra |
| Fő program | `main.py` | Interaktív szimulátor |

## 📁 Fájlszerkezet

```
400km dron test/
├── main.py                      # Fő program — interaktív szimulátor
├── drone.py                     # Drón oldali logika
├── ground_station.py            # Földi állomás
├── radio_channel.py             # HF rádiócsatorna modell
├── telemetry_protocol.py        # Telemetria protokoll
├── automated_test.py            # Automatizált teszt
├── uav_swarm_designer.py        # Drónraj tervező
├── uav_design_output.py         # Tervezési kimenet
├── drone_preview.html           # Drón vizualizáció (HTML)
├── uav_final_spec.json          # Végleges specifikáció
└── README.md
```

## 🚀 Használat

### Interaktív szimulátor indítása

```bash
python main.py
```

### Parancsok

| Billentyű | Művelet |
|-----------|---------|
| `2` | Jamming bekapcsolása 2 MHz-en |
| `3` | Jamming bekapcsolása 3 MHz-en |
| `4` | Jamming bekapcsolása 4 MHz-en |
| `5` | Jamming bekapcsolása 5 MHz-en |
| `c` | Összes jamming törlése |
| `q` | Kilépés |

### Automatizált teszt

```bash
python automated_test.py
```

### Drónraj tervező

```bash
python uav_swarm_designer.py
```

### Kimenet példa

```
==================================================
 DRÓN HF KOMMUNIKÁCIÓ SZIMULÁTOR (2-5 MHz)
==================================================
 Parancsok:
  '2', '3', '4', '5' - Jamming kapcsolása
  'c'                - Összes jamming törlése
  'q'                - Kilépés
==================================================

[2.0 MHz] Drón → Föld: OK | SNR: 12.3 dB
[3.0 MHz] Drón → Föld: JAMMING!! | SNR: -5.2 dB
[4.0 MHz] Drón → Föld: OK | SNR: 10.8 dB
[5.0 MHz] Drón → Föld: OK | SNR: 9.1 dB
```

## 📦 Függőségek

```bash
pip install numpy
```

- **Python 3.8+**
- **numpy** — jelfeldolgozás és fading szimuláció
- **msvcrt** (Windows standard library) — billentyűzet figyelés

## 🔬 Szimulációs modell

### Rádiócsatorna paraméterek

- **Frekvencia:** 2-5 MHz (HF sáv)
- **Távolság:** 400 km
- **Fading:** Rayleigh fading modell
- **Zaj:** Additív fehér Gauss-zaj (AWGN)
- **Moduláció:** Szimulált digitális moduláció

### Telemetria adatok

```
Csomag formátum:
├── Header (azonosító, időbélyeg)
├── Pozíció (GPS koordináták)
├── Sebesség és magasság
├── Akkumulátor státusz
└── Szenzor adatok
```

## 🎯 Alkalmazási terület

- Drón kommunikációs rendszerek tesztelése
- Zavarásszűrési stratégiák fejlesztése
- HF rádiós protokollok validálása
- Katonai/polgári UAV kommunikáció modellezése
