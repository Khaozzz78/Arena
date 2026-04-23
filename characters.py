import random

class Gladiator:
    """Basisklasse für alle Arena-Kämpfer"""
    def __init__(self, name):
        self.name = name
        self.leben = 100
        self.ruestung = 10
        self.ausdauer = 50
        self.geschick = 50
        self.mana = 50
        self.max_leben = 100
        self.block_aktiv = False
    
    def grundangriff(self, ziel):
        if self.ist_bewusstlos():
            return f"{self.name} ist bewusstlos!"
        
        schaden = max(1, 20 - ziel.ruestung)
        if ziel.block_aktiv:
            schaden = schaden // 2
            ziel.block_aktiv = False
            return f"🛡️ {self.name} greift an! {ziel.name} blockt! Nur {schaden} Schaden!"
        else:
            ziel.leben -= schaden
            return f"⚔️ {self.name} greift {ziel.name} an! {schaden} Schaden!"
    
    def blocken(self):
        self.block_aktiv = True
        return f"🛡️ {self.name} geht in Verteidigungsstellung!"
    
    def ist_bewusstlos(self):
        return self.leben <= 0
    
    def status(self):
        hp_bar = "❤️" * (self.leben // 10) + "💔" * ((self.max_leben - self.leben) // 10)
        return f"{self.name}: {hp_bar} ({self.leben}/{self.max_leben} HP)"

class Krieger(Gladiator):
    """Starker Nahkämpfer mit Schwertschlag"""
    def __init__(self, name):
        super().__init__(name)
        self.ruestung += 5
        self.ausdauer += 20
    
    def schwertschlag(self, ziel):
        if self.ist_bewusstlos():
            return f"{self.name} ist bewusstlos!"
        if self.ausdauer < 15:
            
            return f"⚡ {self.name} hat nicht genug Ausdauer für MÄCHTIGER SCHWERTSCHLAG !"
        
        self.ausdauer -= 15
        schaden = max(1, 30 - ziel.ruestung)
        if ziel.block_aktiv:
            schaden = schaden // 2
            ziel.block_aktiv = False
            result = f"⚔️💥 {self.name}: SCHWERTSCHLAG! {ziel.name} blockt! Nur {schaden} Schaden!"
        else:
            result = f"⚔️💥 {self.name}: MÄCHTIGER SCHWERTSCHLAG! {schaden} Schaden!"
        
        ziel.leben -= schaden
        return result

class Magier(Gladiator):
    """Magischer Fernkämpfer mit Feuerball"""
    def __init__(self, name):
        super().__init__(name)
        self.mana += 30
        self.ruestung -= 3
    
    def feuerball(self, ziel):
        if self.ist_bewusstlos():
            return f"{self.name} ist bewusstlos!"
        if self.mana < 20:
            
            return f"🔮 {self.name} hat nicht genug Mana für BRENNENDER FEUERBALL!"
        
        self.mana -= 20
        # Feuer ignoriert Rüstung teilweise
        schaden = max(1, 28 - (ziel.ruestung // 2))
        if ziel.block_aktiv:
            schaden = schaden // 2
            ziel.block_aktiv = False
            result = f"🔥💥 {self.name}: FEUERBALL! {ziel.name} blockt! Nur {schaden} Schaden!"
        else:
            result = f"🔥💥 {self.name}: BRENNENDER FEUERBALL! {schaden} Schaden!"
        
        ziel.leben -= schaden
        return result

class Bogenschuetze(Gladiator):
    """Präziser Fernkämpfer mit Kritischen Treffern"""
    def __init__(self, name):
        super().__init__(name)
        self.geschick += 25
    
    def praezisionsschuss(self, ziel):
        if self.ist_bewusstlos():
            return f"{self.name} ist bewusstlos!"
        if self.geschick < 10:
            return f"🏹 {self.name} hat nicht genug Konzentration!"
        
        self.geschick -= 10
        # 30% Kritische Treffer Chance
        kritisch = random.randint(1, 100) <= 30
        
        if kritisch:
            schaden = max(1, 40 - ziel.ruestung)
            result = f"🏹💀 {self.name}: KRITISCHER TREFFER! {schaden} Schaden!"
        else:
            schaden = max(1, 25 - ziel.ruestung)
            result = f"🏹💥 {self.name}: Präziser Pfeil! {schaden} Schaden!"
        
        if ziel.block_aktiv:
            schaden = schaden // 2
            ziel.block_aktiv = False
            result += f" {ziel.name} blockt! Nur {schaden} wirklicher Schaden!"
        
        ziel.leben -= schaden
        return result