import time
from radio_channel import RadioChannel
from drone import Drone
from ground_station import GroundStation

def run_test_scenario(name, duration_cycles, channel_setup_func):
    print(f"\n" + "="*60)
    print(f" TESZT SZENÁRIÓ INDÍTÁSA: {name}")
    print("="*60)
    
    frequencies = [2, 3, 4, 5]
    channel = RadioChannel(frequencies)
    drone = Drone(channel, frequencies)
    gs = GroundStation(channel)
    
    # Konfiguráljuk a csatornát a szcenáriónak megfelelően
    channel_setup_func(channel)
    
    print(f"[INFO] Helyi Motor EMI aktív: {drone.engine_emi*100}%")
    
    success_count = 0
    for i in range(1, duration_cycles + 1):
        print(f"\n--- Ciklus {i}/{duration_cycles} ---")
        print(f"Csatorna állapot: {channel.get_status()} | Környezeti zaj: {channel.noise_floor*100}%")
        
        success = drone.run_cycle(gs)
        if success:
            success_count += 1
            
    print(f"\n{name} VÉGE.")
    print(f"Sikeres adatátvitel: {success_count}/{duration_cycles} ({ (success_count/duration_cycles)*100:.1f}%)")
    return success_count

def setup_normal(channel):
    channel.noise_floor = 0.05 # Minimális zaj
    print("[SZCENÁRIÓ] Optimális körülmények, tiszta égbolt.")

def setup_bad_weather(channel):
    channel.noise_floor = 0.25 # Közepes zaj (villámlás, statikus zaj)
    print("[SZCENÁRIÓ] Viharos időjárás, erős légköri zaj (QRN).")

def setup_solar_flare(channel):
    channel.noise_floor = 0.5  # 50% csomagvesztés az ionoszféra instabilitása miatt
    channel.set_jamming(2)     # 2 MHz teljesen blokkolva
    channel.set_jamming(4)     # 4 MHz teljesen blokkolva
    print("[SZCENÁRIÓ] !!! EXTRÉM NAPKITÖRÉS ÉS ZAVARÁS !!!")

def setup_multi_jamming(channel):
    channel.noise_floor = 0.05
    channel.set_jamming(2)
    channel.set_jamming(3)
    channel.set_jamming(4)
    print("[SZCENÁRIÓ] Többszörös jamming: Csak az 5 MHz tiszta!")

if __name__ == "__main__":
    # Összes szcenárió futtatása a motorzajjal nehezítve
    run_test_scenario("NORMÁL MŰKÖDÉS (+Motor EMI)", 5, setup_normal)
    run_test_scenario("VIHAROS IDŐJÁRÁS (+Motor EMI)", 5, setup_bad_weather)
    run_test_scenario("KARANTÉN ÉS JAMMING TESZT (+Motor EMI)", 10, setup_multi_jamming)
    run_test_scenario("EXTRÉM NAPKITÖRÉS (+Motor EMI)", 10, setup_solar_flare)
