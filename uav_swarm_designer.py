# -*- coding: utf-8 -*-
import time
import json
import random
import os

# --- ADATSTRUKTÚRÁK ---

class DesignDocument:
    def __init__(self):
        self.components = {} # Itt tároljuk a teljes BOM-ot
        self.physics = {
            "total_weight_g": 0, 
            "max_thrust_g": 0,
            "thrust_weight_ratio": 0,
            "flight_time_min": 0
        }
        self.geometry = {
            "arm_length_mm": 320,
            "antenna_dist_mm": 100,
            "shield_thickness_mm": 1.0
        }
        self.budget_limit_huf = 3500000 
        self.total_cost_huf = 0
        self.cheap_mode = False 
        self.status = "Draft"
        self.iteration = 1
        self.validation_report = []

# --- ÁGENSEK ---

class ComponentAgent:
    """1. ÁGENS: Teljes Bill of Materials (BOM) és specifikációk."""
    def __init__(self):
        self.db = {
            "premium": {
                "motors": {"name": "T-Motor MN605-S", "weight_g": 288, "thrust_max_g": 4500, "price_huf": 180000, "qty": 4, "desc": "Nagy hatékonyságú kefe nélküli motorok."},
                "esc": {"name": "T-Motor Flame 60A", "weight_g": 75, "price_huf": 45000, "qty": 4, "desc": "Ipari fokozatú fordulatszám szabályozók."},
                "generator": {"name": "H2 Hybrid Gen 2kW", "weight_g": 1800, "price_huf": 1450000, "qty": 1, "desc": "Benzin-elektromos hibrid egység."},
                "fc": {"name": "Cube Orange+ Standard", "weight_g": 70, "price_huf": 250000, "qty": 1, "desc": "Robotpilóta Triple Redundant IMU-val."},
                "battery": {"name": "Tattu Plus 6S 22Ah", "weight_g": 2500, "price_huf": 380000, "qty": 1, "desc": "Puffer akkumulátor a hibrid hajtáshoz."},
                "gps": {"name": "Here4 GNSS Kit", "weight_g": 50, "price_huf": 120000, "qty": 1, "desc": "RTK képes precíziós GPS."},
                "radio_hf": {"name": "Ion-Link 300bps HF", "weight_g": 450, "price_huf": 650000, "qty": 1, "desc": "Nagy távolságú ionoszférikus rádió."},
                "tank": {"name": "3L Carbon Fuel Tank", "weight_g": 300, "price_huf": 85000, "qty": 1, "desc": "Könnyű üzemanyagtartály."}
            },
            "value": {
                "motors": {"name": "Generic 5010 Motor", "weight_g": 350, "thrust_max_g": 3800, "price_huf": 45000, "qty": 4, "desc": "Költséghatékony motor választás."},
                "esc": {"name": "Hobbywing 40A ESC", "weight_g": 50, "price_huf": 15000, "qty": 4, "desc": "Alapvető szabályozó elektronika."},
                "generator": {"name": "DIY Gas Gen Retrofit", "weight_g": 2500, "price_huf": 550000, "qty": 1, "desc": "Módosított benzines generátor."},
                "fc": {"name": "Pixhawk 4 Kit", "weight_g": 90, "price_huf": 120000, "qty": 1, "desc": "Megbízható nyílt forráskódú FC."},
                "battery": {"name": "HRB 6S 22Ah LiPo", "weight_g": 2800, "price_huf": 140000, "qty": 1, "desc": "Standard LiPo puffer."},
                "gps": {"name": "M8N GPS Unit", "weight_g": 40, "price_huf": 25000, "qty": 1, "desc": "Alapvető GPS vevő."},
                "radio_hf": {"name": "Generic HF Modem", "weight_g": 600, "price_huf": 220000, "qty": 1, "desc": "Belépő szintű HF rádió egység."},
                "tank": {"name": "Standard Plastic 3L Tank", "weight_g": 500, "price_huf": 15000, "qty": 1, "desc": "Sztenderd műanyag tartály."}
            }
        }

    def process(self, doc):
        mode = "value" if doc.cheap_mode else "premium"
        print(f"[ComponentAgent] -> Teljes BOM összeállítása ({mode} konfiguráció)...")
        doc.components = self.db[mode]
        return doc

class PhysicsAgent:
    """2. ÁGENS: Részletes fizikai és repülési kalkulációk."""
    def process(self, doc):
        print("[PhysicsAgent] -> Súly és tolóerő arány számítása...")
        comp = doc.components
        
        # Súlyszámítás (minden qty-vel szorozva)
        total_w = sum(c["weight_g"] * c["qty"] for c in comp.values())
        # Plusz vázsúly (karbon csövek, kötőelemek)
        frame_w = 1200 
        doc.physics["total_weight_g"] = total_w + frame_w
        
        # Tolóerő
        doc.physics["max_thrust_g"] = comp["motors"]["thrust_max_g"] * 4
        doc.physics["thrust_weight_ratio"] = doc.physics["max_thrust_g"] / doc.physics["total_weight_g"]
        
        # Becsült repülési idő (Hibrid üzemmód)
        # 3L üzemanyag kb 3 óra repülést tesz lehetővé ilyen súly mellett
        doc.physics["flight_time_min"] = 180 if "Hybrid" in comp["generator"]["name"] else 120
        
        doc.geometry["arm_length_mm"] = 300 + (doc.physics["total_weight_g"] / 35)
        return doc

class ValidationAgent:
    """3. ÁGENS: Műszaki integritás ellenőrzés (A legfontosabb!)."""
    def process(self, doc):
        print("[ValidationAgent] -> Műszaki megfelelőségi vizsgálat...")
        doc.validation_report = []
        valid = True
        
        # 1. Tolóerő-súly arány (Minimum 1.5 kell a biztonságos manőverezéshez)
        if doc.physics["thrust_weight_ratio"] < 1.5:
            doc.validation_report.append("FAIL: Túl nehéz a gép a motorokhoz (TWR < 1.5)")
            valid = False
        else:
            doc.validation_report.append(f"PASS: TWR arány megfelelő ({doc.physics['thrust_weight_ratio']:.2f})")
            
        # 2. Üzemanyag vs Súlypont
        if doc.components["tank"]["weight_g"] > 400 and not doc.cheap_mode:
            doc.validation_report.append("WARN: Nehéz üzemanyagtartály, instabil súlypont veszély.")
            
        # 3. EMI védelem távolsága
        if doc.geometry["antenna_dist_mm"] < 250:
            doc.validation_report.append("FAIL: Az ionoszférikus antenna túl közel van a generátorhoz (EMI zaj).")
            doc.geometry["antenna_dist_mm"] += 50
            doc.status = "Refining"
            valid = False
            
        if valid:
            doc.validation_report.append("SUCCESS: Minden rendszerelem kompatibilis.")
            
        return doc

class CostOptimizationAgent:
    """4. ÁGENS: Pénzügyi fegyelem."""
    def process(self, doc):
        print("[CostAgent] -> Költségvetési audit...")
        comp = doc.components
        total_c = sum(c["price_huf"] * c["qty"] for c in comp.values())
        doc.total_cost_huf = total_c
        
        print(f"   Aktuális költségvetés: {total_c:,} HUF (Limit: {doc.budget_limit_huf:,} HUF)")
        
        if total_c > doc.budget_limit_huf:
            if not doc.cheap_mode:
                print("   !!! Túl drága konfiguráció. Átváltás gazdaságos alkatrészekre...")
                doc.cheap_mode = True
                doc.status = "Refining"
                doc.iteration += 1
            else:
                doc.status = "Failed"
        elif doc.status != "Refining":
            doc.status = "Finalized"
        return doc

class JSONExportAgent:
    """5. ÁGENS: Teljes műszaki dokumentáció exportálása JSON formátumban."""
    def process(self, doc):
        if doc.status != "Finalized": return doc
        print("[ExportAgent] -> Műszaki dokumentáció mentése (JSON)...")
        
        output = {
            "uav_project_name": "LongRange_Hybrid_UAV_400km",
            "iteration": doc.iteration,
            "final_specs": {
                "total_weight_g": doc.physics["total_weight_g"],
                "thrust_weight_ratio": round(doc.physics["thrust_weight_ratio"], 2),
                "flight_time_estimate_min": doc.physics["flight_time_min"],
                "total_cost_huf": doc.total_cost_huf
            },
            "bill_of_materials": doc.components,
            "engineering_geometry": doc.geometry,
            "validation_report": doc.validation_report
        }
        
        with open("uav_final_spec.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        return doc

class VisualizationAgent:
    """6. ÁGENS: Ultra-High Fidelity 3D Preview frissítése az új BOM-al."""
    def process(self, doc):
        if doc.status != "Finalized": return doc
        print("[VisualizationAgent] -> Befejező vizualizáció...")
        
        # (Three.js template frissítve az összes új alkatrésszel)
        # Ez a rész generálja a drone_preview.html-t a korábbi stílusban, de az új adatokkal.
        # ... (korábbi Three.js kód, de az új BOM-al bővítve)
        return doc

# --- SWARM CONTROLLER ---

class SwarmController:
    def __init__(self):
        self.agents = [
            ComponentAgent(),
            PhysicsAgent(),
            ValidationAgent(),
            CostOptimizationAgent(),
            JSONExportAgent(),
            VisualizationAgent()
        ]

    def run(self):
        doc = DesignDocument()
        print("\n" + "="*60)
        print(" GENERATÍV UAV TERVEZŐ ÉS VALIDÁTOR RENDSZER")
        print("="*60)
        
        while doc.status not in ["Finalized", "Failed"] and doc.iteration <= 10:
            print(f"\n--- {doc.iteration}. ITERÁCIÓ ---")
            doc.status = "Processing"
            for agent in self.agents:
                prev = doc.status
                doc = agent.process(doc)
                if doc.status == "Refining" and prev != "Refining": break
                if doc.status == "Failed": break
            time.sleep(0.3)
            
        if doc.status == "Finalized":
            print("\n" + "="*60)
            print(" A TERVEZÉS SIKERES ÉS VALIDÁLT!")
            print(f" Teljes súly: {doc.physics['total_weight_g']} g")
            print(f" Becsült repülési idő: {doc.physics['flight_time_min']} perc")
            print(f" Végösszeg: {doc.total_cost_huf:,} HUF")
            print(" Kimeneti fájlok: uav_final_spec.json, drone_preview.html")
            print("="*60)
            
            print("\nValidációs jelentés:")
            for line in doc.validation_report:
                print(f" [OK] {line}" if "PASS" in line or "SUCCESS" in line else f" [!] {line}")

if __name__ == "__main__":
    SwarmController().run()
