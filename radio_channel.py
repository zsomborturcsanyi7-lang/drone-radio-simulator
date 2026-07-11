import random
import time

class RadioChannel:
    """
    Az ionoszférikus rádiócsatorna szimulációja.
    Kezeli a zajszintet, a jelgyengülést és a szándékos zavarást (Jamming).
    """
    def __init__(self, frequencies):
        self.frequencies = frequencies
        self.jammed_frequencies = set()
        self.noise_floor = 0.1  # Alapzaj (0.0 - 1.0)
        
    def set_jamming(self, frequency, active=True):
        """Be- vagy kikapcsolja a zavarást egy adott frekvencián."""
        if active:
            self.jammed_frequencies.add(frequency)
            print(f"!!! JAMMING AKTIVÁLVA: {frequency} MHz !!!")
        else:
            if frequency in self.jammed_frequencies:
                self.jammed_frequencies.remove(frequency)
                print(f"--- Jamming megszűnt: {frequency} MHz ---")

    def transmit(self, payload, frequency, extra_noise=0, use_fec=True):
        """
        Megkísérel átvinni egy csomagot. 
        use_fec: Ha True, a Reed-Solomon javíthat a hibákon.
        """
        if frequency in self.jammed_frequencies:
            return None, False
        
        total_noise = min(1.0, self.noise_floor + extra_noise)
        
        # Véletlenszerű esemény generálása
        roll = random.random()
        
        if roll < total_noise:
            # Alapesetben elveszett, de a FEC megpróbálhatja javítani
            # A 4 bájtos RS paritás kb. a hibák 40%-át tudja helyreállítani HF környezetben
            if use_fec and random.random() < 0.40:
                return payload, True # Visszaadjuk a payload-ot, jelezve hogy FEC mentette meg
            return None, False
            
        return payload, False # Sima vétel hiba nélkül

    def get_status(self):
        """Visszaadja a csatorna aktuális állapotát."""
        status = []
        for f in self.frequencies:
            state = "[JAMMED]" if f in self.jammed_frequencies else "[CLEAR]"
            status.append(f"{f}MHz: {state}")
        return " | ".join(status)
