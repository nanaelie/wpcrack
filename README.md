# WPCrack - Outil de Cracking WiFi
WPCrack est un outil permettant de tester des mots de passe WiFi à partir d'un fichier de capture PCAP en utilisant **Aircrack-ng**. Il essaie les mots de passe d'une liste spécifiée jusqu'à trouver la bonne clé.

## Prérequis
Avant d'utiliser cet outil, assurez-vous d'avoir :
- **Python 3.x** installé
- **Aircrack-ng** installé et accessible dans le PATH
- Une **wordlist** contenant des mots de passe potentiels
- Un fichier de capture **(.pcap, .ivs, .cap)**

## Installation
Clonez le dépôt et accédez au dossier :
```bash
 git clone https://github.com/nanaelie/wpcrack.git
 cd wpcrack
```

## Utilisation
Exécutez le script avec les arguments suivants :
```bash
python3 wpcrack.py --bssid <BSSID> --wlst <wordlist.txt> --file <capture.pcap>
```
### Paramètres :
- `--bssid` : Adresse MAC du point d'accès cible
- `--wlst` : Chemin du fichier contenant la wordlist
- `--file` : Chemin du fichier de capture réseau

## Exemple d'exécution
```bash
python3 wpcrack.py --bssid 00:11:22:33:44:55 --wlst rockyou.txt --file handshake.pcap
```

## Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le redistribuer sous les termes de cette licence.

## Contribution
Les contributions sont les bienvenues !

## Avertissement
**Ce programme est fourni à des fins éducatives uniquement. L'utilisation non autorisée d'outils de pentesting est illégale et punissable par la loi.**
