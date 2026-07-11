from telemetry_protocol import TelemetryProtocol

class GroundStation:
    """
    Földi állomás szimulációja, amely fogadja és feldolgozza a telemetriát.
    """
    def __init__(self, channel):
        self.channel = channel

    def listen(self, frequency):
        """
        Hallgatózik az adott frekvencián.
        Bár a szimulációban a Drone hívja a transmit-ot, 
        ez a metódus szimbolizálja a vétel utáni feldolgozást.
        """
        # A valódi szimulációt a main loop koordinálja, 
        # de itt definiáljuk a feldolgozó logikát.
        pass

    def process_incoming(self, payload):
        """Feldolgozza a beérkező 11 bájtos nyers adatot."""
        if not payload:
            return None
            
        try:
            data = TelemetryProtocol.unpack(payload)
            print(f"[GROUND] Telemetria fogadva:")
            print(f"         Pozíció: {data.latitude:.6f}, {data.longitude:.6f}")
            print(f"         Akku: {data.battery}% | Latency: {data.latency_ms}ms")
            return data
        except Exception as e:
            print(f"[GROUND] HIBA a dekódolás során: {e}")
            return None
