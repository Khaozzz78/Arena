import tkinter as tk
from tkinter import ttk
import random
from characters import Krieger, Magier, Bogenschuetze

class ArenaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏟️ ARENA CHAMPIONS 🏟️")
        self.root.geometry("800x750")  # Etwas höher
        self.root.configure(bg='black')
        
        # ⚔️ ARENA SETUP
        self.spieler = Krieger("Aragorn")
        self.gegner = Magier("Gandalf")
        self.combat_log = []
        
        self.setup_ui()
        self.update_arena_display()
    
    def setup_ui(self):
        # 🎮 TITEL
        title_label = tk.Label(
            self.root, 
            text="⚔️  ARENA CHAMPIONS  ⚔️", 
            font=("Courier", 20, "bold"),
            fg="green", bg="black"
        )
        title_label.pack(pady=20)
        
        # 🏟️ ARENA DISPLAY (HÖHER!)
        self.arena_display = tk.Text(
            self.root,
            height=35, width=80,  # Von 15 auf 20!
            font=("Courier", 10),
            fg="green", bg="black",
            state="disabled"
        )
        self.arena_display.pack(pady=10)
        
        # 🎛️ BUTTON FRAME
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=20)
        
        # ⚔️ ACTION BUTTONS
        self.btn_attack = tk.Button(
            button_frame, text="⚔️ ANGRIFF", 
            font=("Courier", 12, "bold"),
            fg="red", bg="gray20",
            command=self.angriff_clicked,
            width=12
        )
        self.btn_attack.pack(side="left", padx=10)
        
        self.btn_special = tk.Button(
            button_frame, text="⚡ SPEZIAL",
            font=("Courier", 12, "bold"), 
            fg="yellow", bg="gray20",
            command=self.spezial_clicked,
            width=12
        )
        self.btn_special.pack(side="left", padx=10)
        
        self.btn_auto = tk.Button(
            button_frame, text="🤖 AUTO",
            font=("Courier", 12, "bold"),
            fg="cyan", bg="gray20", 
            command=self.auto_clicked,
            width=12
        )
        self.btn_auto.pack(side="left", padx=10)
        
        # 🔄 NEUER KAMPF BUTTON
        self.btn_neuer_kampf = tk.Button(
            button_frame, text="🔄 NEUER KAMPF",
            font=("Courier", 10, "bold"),
            fg="white", bg="gray20", 
            command=self.neuer_kampf_clicked,
            width=14
        )
        self.btn_neuer_kampf.pack(side="left", padx=10)

    def update_display(self, text):
        """Update the main display area"""
        self.arena_display.config(state="normal")
        self.arena_display.delete(1.0, tk.END)
        self.arena_display.insert(tk.END, text)
        self.arena_display.config(state="disabled")
        
    def update_arena_display(self):
        # Check für Kampf-Ende FIRST!
        if self.spieler.ist_bewusstlos() or self.gegner.ist_bewusstlos():
            self.show_sieger()
            return
        
        arena_text = f"""
⚔️  ARENA CHAMPIONS  ⚔️

{self.spieler.status()}

                    🆚
                    
{self.gegner.status()}

═══════════════════════════════════════
COMBAT LOG:
"""
        # Zeige letzte 8 Combat-Nachrichten (statt 5!)
        for nachricht in self.combat_log[-8:]:
            arena_text += f"• {nachricht}\n"
        
        self.update_display(arena_text)
    
    def show_sieger(self):
        """Zeige Sieger-Screen"""
        if self.spieler.ist_bewusstlos():
            sieger = self.gegner.name
            emoji = "🧙‍♂️"
        else:
            sieger = self.spieler.name  
            emoji = "⚔️"
        
        sieger_text = f"""
    🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆

             {emoji} {sieger.upper()} GEWINNT! {emoji}

    🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆

FINALER KAMPFSTAND:
{self.spieler.name}: {max(0, self.spieler.leben)} HP
{self.gegner.name}: {max(0, self.gegner.leben)} HP

═══════════════════════════════════════
KOMPLETTE KAMPF-HISTORIE:
"""
        # Zeige ALLE Combat-Nachrichten vom Kampf
        for nachricht in self.combat_log:
            sieger_text += f"• {nachricht}\n"
        
        sieger_text += f"""
═══════════════════════════════════════

          🔄 Klicke "NEUER KAMPF" für Revanche! 🔄
"""
        
        self.update_display(sieger_text)
    
    def angriff_clicked(self):
        if self.spieler.ist_bewusstlos() or self.gegner.ist_bewusstlos():
            return
        
        # Spieler greift an
        nachricht = self.spieler.grundangriff(self.gegner)
        self.combat_log.append(nachricht)

        # Gegner kontert
        if not self.gegner.ist_bewusstlos():
            if self.gegner.mana >= 20:
                gegner_aktion = self.gegner.feuerball(self.spieler)
            else:
                gegner_aktion = self.gegner.grundangriff(self.spieler)
            self.combat_log.append(gegner_aktion)

        self.update_arena_display()

    def spezial_clicked(self):
        if self.spieler.ist_bewusstlos() or self.gegner.ist_bewusstlos():
            return
            
        # Spieler versucht Spezialangriff
        nachricht = self.spieler.schwertschlag(self.gegner)
        self.combat_log.append(nachricht)
        
        # Wenn Ausdauer zu wenig war, mach zusätzlich Grundangriff
        if "nicht genug Ausdauer" in nachricht:
            fallback = self.spieler.grundangriff(self.gegner)
            self.combat_log.append(fallback)
        
                
        # Gegner kontert
        if not self.gegner.ist_bewusstlos():
            if self.gegner.mana >= 20:
                gegner_aktion = self.gegner.feuerball(self.spieler)
            else:
                gegner_aktion = self.gegner.grundangriff(self.spieler)
            self.combat_log.append(gegner_aktion)
        
        self.update_arena_display()
    
    def auto_clicked(self):
        self.update_display("🤖 AUTO-MODUS aktiviert! (Coming soon...)")
    
    def neuer_kampf_clicked(self):
        """Reset für neuen Kampf"""
        self.spieler = Krieger("Aragorn")
        self.gegner = Magier("Gandalf") 
        self.combat_log = []
        self.update_arena_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArenaGUI(root)
    root.mainloop()