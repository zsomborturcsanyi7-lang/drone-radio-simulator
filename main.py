import time
import sys
import msvcrt # Windows-specifikus a billentyűzet figyeléséhez
from radio_channel import RadioChannel
from drone import Drone
from ground_station import GroundStation

def print_help():
    print("\n" + "="*50)
    print(" DRÓN HF KOMMUNIKÁCIÓ SZIMULÁTOR (2-5 MHz)")
    print("="*50)
    print(" Parancsok:")
    print("  '2', '3', '4', '5' - Jamming kapcsolása az adott frekvencián")
    print("  'c'              - Összes jamming törlése")
    print("  'q'              - Kilépés")
    print("="*50)

def main():
    frequencies = [2, 3, 4, 5]
    channel = RadioChannel(frequencies)
    drone = Drone(channel, frequencies)
    gs = GroundStation(channel)
    
    print_help()
    
    last_cycle_time = 0
    cycle_interval = 5 # 5 másodperces ciklusok
    
    running = True
    while running:
        # Billentyűzet figyelése (non-blocking)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'q':
                running = False
                continue
            elif key in ['2', '3', '4', '5']:
                f = int(key)
                # Toggle jamming
                is_jammed = f in channel.jammed_frequencies
                channel.set_jamming(f, not is_jammed)
            elif key == 'c':
                channel.jammed_frequencies.clear()
                print("--- Összes csatorna megtisztítva ---")
        
        # Szimulációs ciklus futtatása 5 másodpercenként
        current_time = time.time()
        if current_time - last_cycle_time >= cycle_interval:
            print(f"\n[IDŐ: {time.strftime('%H:%M:%S')}] Csatorna állapot: {channel.get_status()}")
            
            # A drón megkísérli a küldést
            drone.run_cycle(gs)
            
            last_cycle_time = current_time
            
        # Kis pihentetés a CPU kímélése érdekében
        time.sleep(0.1)

    print("\nSzimuláció leállítva.")

if __name__ == "__main__":
    main()
