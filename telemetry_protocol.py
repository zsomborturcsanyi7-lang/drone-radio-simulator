import struct
from dataclasses import dataclass

@dataclass
class TelemetryData:
    latitude: float  # Fixpontos konverzió előtt
    longitude: float # Fixpontos konverzió előtt
    battery: int     # 0-100
    latency_ms: int  # ezredmásodperc

class TelemetryProtocol:
    # 'i' = 4 byte (Lat), 'i' = 4 byte (Lon), 'B' = 1 byte (Bat), 'H' = 2 byte (Latency)
    # + '4s' = 4 byte Reed-Solomon Parity (szimulált)
    # Összesen: 11 + 4 = 15 byte
    FORMAT = "!iiBH4s"
    
    SCALE = 10**7

    @staticmethod
    def pack(data: TelemetryData) -> bytes:
        """Becsomagolja az adatokat + FEC paritás bájtokat ad hozzá."""
        lat_fixed = int(data.latitude * TelemetryProtocol.SCALE)
        lon_fixed = int(data.longitude * TelemetryProtocol.SCALE)
        
        # Szimulált paritás bájtok (valóságban RS algoritmus generálná)
        parity = b"FEC!" 
        
        return struct.pack(
            TelemetryProtocol.FORMAT,
            lat_fixed,
            lon_fixed,
            data.battery,
            data.latency_ms,
            parity
        )

    @staticmethod
    def unpack(payload: bytes):
        """Kicsomagolja az adatokat és ellenőrzi a paritást."""
        try:
            lat_fixed, lon_fixed, battery, latency_ms, parity = struct.unpack(
                TelemetryProtocol.FORMAT,
                payload
            )
            
            return TelemetryData(
                latitude=lat_fixed / TelemetryProtocol.SCALE,
                longitude=lon_fixed / TelemetryProtocol.SCALE,
                battery=battery,
                latency_ms=latency_ms
            )
        except Exception:
            return None

if __name__ == "__main__":
    # Egyszerű teszt
    test_data = TelemetryData(47.4979, 19.0402, 85, 120)
    packed = TelemetryProtocol.pack(test_data)
    print(f"Becsomagolt méret: {len(packed)} bájt")
    print(f"Nyers bájtok: {packed.hex()}")
    
    unpacked = TelemetryProtocol.unpack(packed)
    print(f"Visszafejtve: {unpacked}")
