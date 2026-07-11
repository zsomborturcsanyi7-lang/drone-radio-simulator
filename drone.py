import time
from telemetry_protocol import TelemetryProtocol, TelemetryData

class Drone:
    """
    Az autonóm drón szimulációja ALE (Automatic Link Establishment) képességgel
    és frekvencia karantén funkcióval.
    """
    def __init__(self, channel, frequencies):
        self.channel = channel
        self.frequencies = frequencies
        self.current_freq_index = 0
        self.missed_pongs = 0
        self.max_missed = 3
        
        # FIZIKAI ÁRNYÉKOLÁS: Faraday-kalitka és távoli antenna
        self.shielding_active = True
        self.engine_emi = 0.02 # 20%-ról 2%-ra csökkentve az árnyékolás miatt
        
        # SZOFTVERES FEC: Reed-Solomon kódolás aktív
        self.fec_enabled = True
        
        # Karantén adatok: frequency -> expiration_timestamp
        self.quarantine = {}
        self.quarantine_duration = 120 # 2 perc
        
        # Kezdeti állapot adatok
        self.lat = 47.4979
        self.lon = 19.0402
        self.battery = 100
        self.latency = 0

    @property
    def current_frequency(self):
        return self.frequencies[self.current_freq_index]

    def update_telemetry(self):
        """Szimulált mozgás és merülés."""
        self.lat += 0.0001
        self.lon += 0.0001
        self.battery = max(0, self.battery - 0.1)
        self.latency = 120 + (self.missed_pongs * 50)

    def run_cycle(self, ground_station):
        """Egy kommunikációs ciklus lefuttatása (Ping -> Wait Pong)."""
        self.update_telemetry()
        
        current_freq = self.current_frequency
        if current_freq in self.quarantine:
            if time.time() < self.quarantine[current_freq]:
                remaining = int(self.quarantine[current_freq] - time.time())
                print(f"[DRONE] HIBA: A jelenlegi frekvencia ({current_freq} MHz) karanténban van még {remaining} mp-ig!")
                self.hop_frequency()
                return False
            else:
                print(f"[DRONE] INFO: {current_freq} MHz karanténja lejárt, újra próbálkozunk.")
                del self.quarantine[current_freq]

        data = TelemetryData(
            latitude=self.lat,
            longitude=self.lon,
            battery=int(self.battery),
            latency_ms=self.latency
        )
        
        payload = TelemetryProtocol.pack(data)
        freq = self.current_frequency
        
        print(f"\n[DRONE] Adás indítása {freq} MHz-en... (Helyi EMI: {self.engine_emi*100}%)")
        
        # Küldés FEC-el
        received_payload, fec_saved = self.channel.transmit(payload, freq, 
                                                           extra_noise=self.engine_emi, 
                                                           use_fec=self.fec_enabled)
        
        if received_payload:
            if fec_saved:
                print("[INFO] !!! SZOFTVERES JAVÍTÁS (FEC) SIKERES: A telemetria megérkezett a zaj ellenére! !!!")
            
            ground_station.process_incoming(received_payload)
            
            # Pong vétel
            pong, pong_fec_saved = self.channel.transmit(b"PONG", freq, 
                                                        extra_noise=self.engine_emi, 
                                                        use_fec=self.fec_enabled)
            
            if pong:
                if pong_fec_saved:
                    print("[INFO] !!! SZOFTVERES JAVÍTÁS (FEC) SIKERES: A PONG megérkezett! !!!")
                print(f"[DRONE] PONG érkezett! Kapcsolat stabil @ {freq} MHz")
                self.missed_pongs = 0
                return True
            else:
                print(f"[DRONE] HIBA: Telemetria elment, de a PONG elveszett!")
        else:
            print(f"[DRONE] HIBA: A telemetria csomag nem ért célba!")
        
        self.missed_pongs += 1
        print(f"[DRONE] Sikertelen kísérlet ({self.missed_pongs}/{self.max_missed})")
        
        if self.missed_pongs >= self.max_missed:
            self.quarantine[freq] = time.time() + self.quarantine_duration
            print(f"[DRONE] !!! {freq} MHz KARANTÉNBA KERÜLT (120 mp) !!!")
            self.hop_frequency()
            
        return False

    def hop_frequency(self):
        """Frekvenciaváltás az elérhető (nem karanténolt) frekvenciák közül."""
        start_index = self.current_freq_index
        
        # Megpróbáljuk megkeresni a következő olyan frekvenciát, ami nincs karanténban
        for _ in range(len(self.frequencies)):
            self.current_freq_index = (self.current_freq_index + 1) % len(self.frequencies)
            freq = self.current_frequency
            
            # Ha nincs karanténban, vagy lejárt a karantén
            if freq not in self.quarantine or time.time() >= self.quarantine[freq]:
                if freq in self.quarantine:
                    del self.quarantine[freq]
                print(f"[DRONE] !!! ALE AKTIVÁLVA: Új frekvencia -> {freq} MHz !!!")
                self.missed_pongs = 0
                return
        
        # Ha minden frekvencia karanténban van, akkor kénytelenek vagyunk a következőre ugrani 
        # (vagy várni, de itt most ugrunk és jelezzük a vészhelyzetet)
        self.current_freq_index = (start_index + 1) % len(self.frequencies)
        print(f"[DRONE] FIGYELEM: Minden frekvencia rossz! Kényszerített ugrás -> {self.current_frequency} MHz")
        self.missed_pongs = 0
