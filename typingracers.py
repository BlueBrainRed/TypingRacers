#!/usr/bin/env python3
import curses
import time
import ctypes
from colorama import Fore
import pygame
import sys
import os
import shutil
import time_attack
import pyfiglet

CHECKERED_FLAG = r"""
   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠐⠒⠂⠐⠄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠰⣶⣿⣿⣿⣿⣆⠀⠀⠀⠀  ⠘⡄⠀⠀⠀⠀⠀⠀⠀
⢤⣤⣤⣴⣶⣎⠉⠀⠀⠀⠀⠹⣿⣿⣿⣿⡿⠆⣤⣤⣤⣶⣾⡀⠀⠀⠀⠀⠀⠀
⠈⢿⣿⣿⣿⣿⣆⠀⠀⠀⠀⣀⣽⠋⠉⠀⠀ ⠀⠹⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀
⠀⠈⣿⠿⠿⠿⠟⠢⣴⣾⣿⣿⣿⣦⠀⠀⠀⠀ ⠀⢹⠿⠿⠿⠿⠳⡀⠀⠀⠀⠀
⠀⠀⠘⡄⠀⠀⠀⠀⠹⣿⣿⣿⣿⡿⠧⣤⣶⣾⣿⣿⣆⠀⠀⠀⠀  ⢱⠀⠀⠀⠀
⠀⠀⠀⠘⡄⠀⠀⠀⢀⣸⠟⠉⠁⠀⠀⠘⣿⣿⣿⣿⣿⣆⠀⠀  ⠀⠀⢣⠀⠀⠀
⠀⠀⠀⠀⠘⣶⣶⣿⣿⣿⣧⠀⠀⠀⠀⢀⣈⡟⠛⠉⠉ ⠀⠹⣿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⡧⢠⣴⣾⣿⣿⣷⡀⠀⠀ ⠀⠀⠙⣿⣿⣿⣿⣆⠀
⠀⠀⠀⠀⠀⠀⠹⡟⠛⠉⠀⠀⠈⢿⣿⣿⣿⣿⣿⡤⠤ ⠀⠒⠒⠚⠛⢻⠛⠿⠆
⠀⠀⠀⠀⠀⠀⠀⠡⠀⠀⠀⠀⠀ ⢀⡻⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀  ⠀  ⠢⠒⠈
⠀⠀⠀⠀⠀⠀⠀⠀⠣⣀⠠⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
CAR_ASCII = '''"ō͡≡o˞_'''
def resource_path(relative_path):
    """
    Retourne le chemin absolu vers une ressource, que l'application soit exécutée en mode développement
    ou en tant qu'exécutable PyInstaller.
    """
    try:
        # PyInstaller crée un dossier temporaire et y stocke les ressources.
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def typewriter(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
def typewriter_centered(text, delay=0.05):
    # Récupérer la largeur du terminal
    term_size = shutil.get_terminal_size()
    width = term_size.columns

    # Découper le texte en lignes et centrer chaque ligne
    lines = text.splitlines()
    for line in lines:
        centered_line = line.center(width)
        for char in centered_line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
    sys.stdout.flush()
def clear_fast():
    print(" \n" * 100)
def maximize_console_window():
    VK_MENU = 0x12  # Touche Alt
    VK_RETURN = 0x0D  # Touche Entrée
    KEYEVENTF_KEYDOWN = 0
    KEYEVENTF_KEYUP = 0x0002
    """
        Simule la combinaison Alt+Enter pour tenter de passer en plein écran.
        Utilise la fonction keybd_event de l'API Win32.

        Remarque : Cette méthode peut ne pas fonctionner sur toutes les versions de Windows,
        surtout sur Windows 10/11 où le mode plein écran console n'est plus supporté de la même manière.
        """
    user32 = ctypes.windll.user32

    # Appuyer sur Alt
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    # Appuyer sur Entrée
    user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    # Relâcher Entrée
    user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    # Relâcher Alt
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
def typing_racers(stdscr):
    """Tutoriel TYPING RACERS avec interface embellie."""

    # Configuration initiale de curses
    curses.curs_set(0)       # Masquer le curseur
    stdscr.nodelay(False)    # Lecture bloquante (on attend la frappe)
    curses.start_color()

    # Paires de couleurs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Texte correct
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Texte incorrect
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Texte standard
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Décor (drapeaux, cadre)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Stats / titres
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Banner

    # Banner ASCII (titre principal)
    banner_text = pyfiglet.figlet_format("TYPING RACERS", font="slant")

    # Texte à taper
    text_to_type = (
        "Bonjour, bienvenue dans TYPING RACERS ! "
        "Tapez ce texte correctement pour faire avancer la voiture."
    )
    track_length = 50  # Longueur de la piste ASCII

    # Variables pour le texte affiché et les stats cumulatives
    typed_text = []    # Texte actuellement affiché (modifié par Backspace)
    total_inputs = 0   # Compteur de toutes les frappes (sans réinitialisation)
    correct_inputs = 0 # Compteur de frappes correctes (incrémenté même si l’erreur est corrigée)
    start_time = time.time()

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # -- 1) Afficher la bannière en haut, centrée --
        banner_lines = banner_text.splitlines()
        for i, line in enumerate(banner_lines):
            x = max(0, (w - len(line)) // 2)
            stdscr.addstr(i, x, line, curses.color_pair(6) | curses.A_BOLD)

        top_area = len(banner_lines) + 1  # Y de départ sous la bannière

        # -- 2) Afficher les drapeaux à damier à gauche et à droite --
        flag_lines = CHECKERED_FLAG.splitlines()
        flag_width = max(len(fl) for fl in flag_lines)

        # Drapeau gauche
        for i, line in enumerate(flag_lines):
            if top_area + i < h - 1:
                stdscr.addstr(top_area + i, 1, line, curses.color_pair(4))

        # Drapeau droit
        for i, line in enumerate(flag_lines):
            if top_area + i < h - 1:
                x = w - flag_width - 2
                stdscr.addstr(top_area + i, x, line, curses.color_pair(4))

        # -- 3) Dessiner un cadre au centre pour la zone de jeu --
        box_top = top_area
        box_bottom = h - 2
        box_left = flag_width + 3
        box_right = w - flag_width - 4
        if box_right <= box_left:
            # Si l'écran est trop petit, on ajuste
            box_left = 2
            box_right = w - 3

        # Lignes horizontales
        for x in range(box_left, box_right):
            stdscr.addch(box_top, x, curses.ACS_HLINE, curses.color_pair(4))
            stdscr.addch(box_bottom, x, curses.ACS_HLINE, curses.color_pair(4))
        # Lignes verticales
        for y in range(box_top, box_bottom + 1):
            stdscr.addch(y, box_left, curses.ACS_VLINE, curses.color_pair(4))
            stdscr.addch(y, box_right, curses.ACS_VLINE, curses.color_pair(4))
        # Coins
        stdscr.addch(box_top, box_left, curses.ACS_ULCORNER, curses.color_pair(4))
        stdscr.addch(box_top, box_right, curses.ACS_URCORNER, curses.color_pair(4))
        stdscr.addch(box_bottom, box_left, curses.ACS_LLCORNER, curses.color_pair(4))
        stdscr.addch(box_bottom, box_right, curses.ACS_LRCORNER, curses.color_pair(4))

        # Espace intérieur du cadre
        inner_left = box_left + 2
        inner_top = box_top + 2

        # -- 4) Calcul de la progression pour la voiture --
        typed_index = 0
        for i, ch in enumerate(typed_text):
            if i < len(text_to_type) and ch == text_to_type[i]:
                typed_index += 1
            else:
                break

        progress_ratio = typed_index / len(text_to_type) if text_to_type else 0
        car_position = int(progress_ratio * track_length)

        # -- 5) Calcul des stats --
        elapsed = time.time() - start_time
        accuracy = (correct_inputs / total_inputs) * 100 if total_inputs > 0 else 0
        cpm = (typed_index / elapsed) * 60 if elapsed > 0 else 0

        # -- 6) Affichage du contenu dans le cadre --
        # Titre
        stdscr.addstr(inner_top, inner_left, "TUTORIEL TYPING RACERS", curses.color_pair(5) | curses.A_BOLD)

        # Texte à taper
        stdscr.addstr(inner_top + 2, inner_left, "Texte à taper :", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(inner_top + 3, inner_left, text_to_type, curses.color_pair(3))

        # Texte saisi
        stdscr.addstr(inner_top + 5, inner_left, "Texte saisi :", curses.color_pair(3) | curses.A_BOLD)
        for i, ch in enumerate(typed_text):
            color = curses.color_pair(1) if (i < len(text_to_type) and ch == text_to_type[i]) else curses.color_pair(2)
            stdscr.addstr(inner_top + 6, inner_left + i, ch, color)

        # Piste
        track_line = "[" + " " * car_position + CAR_ASCII + " " * max(track_length - car_position, 0) + "] FINISH"
        stdscr.addstr(inner_top + 8, inner_left, track_line, curses.color_pair(4))

        # Stats
        stats_str = f"Temps : {elapsed:.2f}s | Accuracy : {accuracy:.2f}% | CPM : {cpm:.1f}"
        stdscr.addstr(inner_top + 10, inner_left, stats_str, curses.color_pair(5))

        # Instructions
        instr_str = "Tapez le texte. (Utilisez Backspace pour corriger, erreurs comptabilisées.)"
        stdscr.addstr(inner_top + 12, inner_left, instr_str, curses.color_pair(3))

        # Indication de sortie
        stdscr.addstr(box_bottom, inner_left, "[ESC pour quitter]", curses.color_pair(3))

        # -- 7) Vérification de fin --
        if typed_index == len(text_to_type):
            # On affiche un message de réussite
            msg = "FÉLICITATIONS, vous avez terminé ! Appuyez sur une touche..."
            stdscr.addstr(inner_top + 14, inner_left, msg, curses.color_pair(1) | curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            break

        stdscr.refresh()

        # -- 8) Gestion des touches --
        key = stdscr.getch()
        if key == 27:  # ESC
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if typed_text:
                typed_text.pop()
        else:
            try:
                ch = chr(key)
            except ValueError:
                ch = ''
            if ch:
                total_inputs += 1
                pos = len(typed_text)
                if pos < len(text_to_type) and ch == text_to_type[pos]:
                    correct_inputs += 1
                typed_text.append(ch)

def start_musique_intro():
    pygame.init()
    pygame.mixer.init()
    intro_music_path1 = resource_path("intro.mp3")
    pygame.mixer.music.load(intro_music_path1)
    pygame.mixer.music.play(-1)
def stop_musique():
    pygame.mixer.music.stop()

def intro():
    clear_fast()
    logs = [
        "[OK] Initializing kernel modules...",
        "[OK] Starting services...",
        "[OK] Loading system resources...",
        "[OK] Checking system integrity...",
        "[OK] Starting system services...",
        "[OK] Loading system configuration...",
        "[OK] Loading system drivers...",
        "[OK] Network interface eth0 up",
        "[OK] Connecting to DNS server...",
        "[OK] Mounting file systems...",
        "[OK] Checking disk integrity...",
        "[OK] NTP synchronization completed.",
        "[OK] Starting background services...",
        "[OK] Firewall started successfully.",
        "[OK] Loading user profile...",
        "[OK] Initializing graphical interface...",
        "[OK] Missiles launcher ready to fire.",
        "[OK] System startup completed successfully.",

        "Please, wait..."
    ]

    for log in logs:
        print(Fore.GREEN + log)
        time.sleep(0.00000008)
    time.sleep(3)
    clear_fast()
    start_musique_intro()
    typewriter_centered(Fore.YELLOW +
                        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣠⣤⣤⣤⣴⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢞⣷⣻⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣠⣤⣤⣤⣤⣴⣴⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣟⣿⣿⣽⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⣀⣀⣀⣀⣠⣤⣤⣤⣴⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⣞⣿⢯⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⣞⣯⢿⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣠⣄⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣻⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣾⡽⣾⣟⡾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
 ███████████ █████ █████ ███████████  █████ ██████   █████   █████████     ███████████     █████████     █████████  ██████████ ███████████    █████████ 
░█░░░███░░░█░░███ ░░███ ░░███░░░░░███░░███ ░░██████ ░░███   ███░░░░░███   ░░███░░░░░███   ███░░░░░███   ███░░░░░███░░███░░░░░█░░███░░░░░███  ███░░░░░███
░   ░███  ░  ░░███ ███   ░███    ░███ ░███  ░███░███ ░███  ███     ░░░     ░███    ░███  ░███    ░███  ███     ░░░  ░███  █ ░  ░███    ░███ ░███    ░░░ 
    ░███      ░░█████    ░██████████  ░███  ░███░░███░███ ░███             ░██████████   ░███████████ ░███          ░██████    ░██████████  ░░█████████ 
    ░███       ░░███     ░███░░░░░░   ░███  ░███ ░░██████ ░███    █████    ░███░░░░░███  ░███░░░░░███ ░███          ░███░░█    ░███░░░░░███  ░░░░░░░░███
    ░███        ░███     ░███         ░███  ░███  ░░█████ ░░███  ░░███     ░███    ░███  ░███    ░███ ░░███     ███ ░███ ░   █ ░███    ░███  ███    ░███
    █████       █████    █████        █████ █████  ░░█████ ░░█████████     █████   █████ █████   █████ ░░█████████  ██████████ █████   █████░░█████████ 
   ░░░░░       ░░░░░    ░░░░░        ░░░░░ ░░░░░    ░░░░░   ░░░░░░░░░     ░░░░░   ░░░░░ ░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░  ░░░░░░░░░  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣠⣠⣄⣤⣤⣤⣤⣶⣦⣶⣴⣶⣶⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⡿⣿⢿⡿⣿⣟⣿⣿⣻⣟⣻⣏⣿⣭⣯⣽⣭⣿⣼⣧⣿⣾⣷⣾⣶⣷⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⡿⣿⣿⣿⣽⢾⣿⣟⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣽⡿⣯⣿⣟⣾⣟⣿⣽⣯⣿⣟⣯⣷⣿⣻⣾⣟⣷⣿⣻⣿
⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⠿⡿⠿⠿⠿⠟⠟⣛⠛⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⣿⠿⡿⢿⠿⡻⡟⢿⣻⣛⣟⣻⣛⣛⣛⣛⣿⣯⣽⣭⣭⣭⣭⣭⣷⣭⣿⣾⣽⣷⣾⣿⣿⣾⣷⣿⣿⣿⣿⣿⣿⣿⢾⡿⣾⣻⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣟⣾⡿⣟⣷⣿⣻⣾⣟⣷⣿⣳⡿⣯⣷⣿⣻⣷⡿⣟⣾⣿⣽
⠟⡻⢛⠛⠛⡝⢫⠙⡉⠋⠍⠉⠌⠁⠃⠈⠐⠀⠂⠐⠀⠂⠀⠐⠀⠀⠈⠀⠀⠀⠀⣿⣿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣭⣷⣿⣶⣿⣶⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⣿⢿⠿⣿⠿⣿⣿⣟⡿⣻⣛⣟⣻⣛⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣽⡿⣟⣿⡾⣟⣷⣿⣻⣾⣟⣿⣟⣷⡿⣯⣷⣿⡿⣿⣽⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣿⣿⢿⡾⠿⠿⠿⠿⡿⠿⣛⡻⣟⠿⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⢿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣯⣿⣝⣯⣽⣯⣽⣭⣯⣽⣽⣾⣷⣷⣾⣾⣷⣿⣿⣾⣷⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⡅⠀⠀   -- Train your typing Skills --⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⡈⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣯⣧⣰⢂⣶⣿⡿⣿⣻⣟⣻⣛⣟⣻⣛⣟⣛⣛⣛⣛⣟⣻⢛⡟⣻⠟⡿⡻⢶⣶⠶⠾⣿⢷⣯⣭⣭⣭⣯⣿⣝⣻⣿⣿⣿⣟⡿⣻⡟⣿⣟⣟⣻⣛⣟⣯⣻⣭⣯⣯⣿⣽⣿⣿⣽⣯⣯⣽⣭⣯⣽⣭⣿⣽⣿⣿⣽⣾⣿⣟⣿⠆⠀-- A Bermuda Triangle Corp. Production --⠀⠀⠂⠄⣿⣿⣿⣿⣿⣿⣽⣾⡿⣷⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠛⠋⠉⠀⣴⠃⣼⣿⡷⣟⡷⣽⣞⣷⣻⣞⣷⣻⢾⡽⣯⣟⡾⣾⣵⣻⢾⣵⣻⣳⣝⡳⣞⣻⣳⣟⣷⣎⣟⡻⣿⣿⣿⣿⣿⣿⣯⣭⣉⣙⢛⣛⡛⠻⠿⢿⣿⣿⣿⣿⡿⣿⢿⡿⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣾⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠰⣿⣿⣿⣿⣿⣿⣯⣿⣿⢿⣯⣿⣿⣿⣻⣿⣟⣯⣿⣿⣽⣿⡿⣿⣿⣿⣯⣿''',delay=0.0001)
    time.sleep(3)
    typewriter_centered(Fore.YELLOW +'''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢏⠀⠄⢀⣈⢰⡏⢠⣿⣿⣿⣻⡿⣷⣻⣾⢷⣿⡾⣽⣯⢿⡷⣯⣟⣷⢯⣟⡿⣞⡷⣯⡏⣴⠲⣔⠦⣞⢮⡍⣍⠻⣶⣣⢏⡿⣻⣿⣿⣿⣿⣿⣶⣦⣉⢣⡅⡤⠘⠻⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣾⣿⣿⣟⣿⣽⣿⣟⣿⣿⣻⣽⣿⣷⣿⣿⣷⣿⡿⣿
⣶⣶⣦⣤⣤⣤⣤⣤⣄⣄⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠃⠀⣀⣴⡏⠁⣾⠀⣼⣿⣿⣟⣿⣿⣿⣿⣾⣿⣽⣻⣽⢯⡿⡽⢯⠟⡾⢯⠻⡽⣛⠟⡷⠿⢷⠿⣽⣾⣿⣺⡾⣵⢯⢿⣭⠿⣜⣧⡻⣽⢿⣿⣿⣿⣿⣿⣦⣌⡐⣩⠒⣂⠛⠿⣿⣿⣿⣿⣭⣿⣽⣽⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢸⣿⣿⣿⣿⣿⣿⣿⣻⣿⣟⣿⣿⣿⣿⣻⣿⣿⣻⣿⡿⣿⣾⣿⣿⣽⣷⣿⣿
⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠛⠛⠿⠿⠿⣷⠄⠀⠀⠀⠀⢠⣾⡿⠁⠊⣠⣿⠞⣉⣽⡇⢀⣿⣿⣿⣿⣯⣿⣽⣏⣿⣿⣿⣿⣾⣯⣷⡿⣯⢿⣽⣞⡿⣵⢯⡿⡽⢯⡟⡾⣵⢲⣭⡝⣻⣽⣫⣟⣾⢻⡽⣶⣻⡼⣫⡟⣿⣿⣿⣿⣿⣿⣿⣖⡉⠶⠌⡖⢤⠙⠿⣿⣿⣿⣿⣿⣻⣟⣿⣻⣟⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣾⣿⣿⣿⣽⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿
⠀⠄⡈⢀⠠⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠂⠀⠀⠐⠛⠛⠳⢦⣜⣻⣿⠞⣩⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⣻⣿⣷⣿⡿⣿⣿⣿⣿⣷⣾⣼⣳⢮⡷⣾⣵⣳⡾⣵⢮⣿⢡⣘⣿⡿⣯⣟⣾⢿⣧⢻⣷⣻⣵⣻⣵⣛⡿⣿⣿⣿⣿⣿⣿⣶⡒⣎⡲⣬⣶⣳⣊⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢾⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣟⣯⣿⣾⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⠄⣀⡀⠀⠀⠀⠀⠀⠈⢿⣄⣼⠋⡿⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢿⣿⣿⣿⣽⣇⡯⣽⣭⣯⣿⣯⣷⣭⣿⣿⣿⣿⣿⣟⣿⣦⣹⣷⣯⣷⢾⣧⣻⢎⡿⣿⣿⣿⣿⣿⣷⣦⣾⢣⡔⢤⡉⠷⣆⡙⠿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⣽⣿⣿⣿⢶⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠠⢀⣀⠉⢉⠀⠀⠀⢀⣈⠿⠃⣸⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡿⣿⣿⡿⣿⣯⣿⣿⣭⣛⠿⣿⣿⣿⣿⣿⣇⡚⡩⢭⡙⡌⢳⣦⣉⠻⣿⣿⠛⠛⠛⠛⠿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠈⠿⣶⣦⣤⣆⣄⣰⡶⠾⠛⠿⢦⡄⣻⡇⠀⣿⣿⣿⡿⣿⢿⡿⢿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣶⣯⣿⣵⣿⣿⣿⣿⣿⣿⣷⣧⣯⣽⣦⣝⣶⣧⣝⣻⣷⡀⠑⣏⢲⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢆⠀⠀⠉⠛⣹⣿⣟⠛⠛⠛⠻⣾⠓⠋⠁⠀⠐⠻⠶⠴⣶⣶⣿⣿⣫⢟⡻⢛⠾⣛⠛⢫⢛⡙⢏⠛⡹⢋⠛⡝⢯⣛⣍⣛⣛⣿⣛⣛⢻⣞⣓⣛⣛⣟⣻⣟⡿⣿⠿⡿⠿⠿⠿⠿⠿⠽⠿⠿⠿⠿⠿⠿⠿⠿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣯⣿⣶⣭⡟⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣯⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢏⣷⣀⠀⠀⠈⣇⠀⢆⠀⠀⠀⠀⠀⠀⠀⠉⠹⠿⠿⣷⣾⣶⢶⡾⢷⡾⡾⣾⢿⣷⠿⢿⣹⡏⣿⣹⣿⣿⣏⣹⣿⣿⣿⣏⡁⣰⣶⣷⣾⣶⣶⣶⣶⣶⣶⣶⡶⣶⣶⣶⣶⣶⣶⢷⡾⢷⡿⣶⢷⣶⣶⣶⡾⣾⣶⣷⣾⣿⣿⣿⣷⣿⣇⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠁⡀⠄⠀⠡⠀⠀⣠⣟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠁⠑⠲⢬⣝⡻⢶⣄⠈⠳⣈⢣⡀⠀⠀⠀⠀⠀⡠⠖⠀⠀⠀⠈⡙⠶⣄⡀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠛⠛⠛⠿⢷⣽⡎⠷⠿⠾⠧⢿⣶⣽⣶⣹⣖⣳⣮⣷⣫⣟⡷⣛⡷⣛⡾⣖⣻⣼⣳⠾⣵⡿⣛⢯⣽⣷⣼⣞⣼⡷⠟⢯⣀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠈⡐⠀⠄⢂⡁⠐⢠⣟⡏⠀⠀⠀⠀⣈⣟⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠻⢯⣗⣯⡄⢳⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠈⠑⠺⠽⣷⣦⣤⣀⣄⣀⣀⡀⠀⠀⠀⠀⠰⠦⠤⣄⡀⠀⠀⠀⠀⠀⠀⠈⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠉⠉⠉⠙⠛⠛⠛⠷⠿⠷⢮⣷⣿⣏⣵⡙⡎⢭⡹⠏⠉⠋⠛⠛⠛⠻⠳⠈⠙⠓⠶⠶⠶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠂⠄⡡⠐⣀⢂⡁⢸⡇⣷⣦⠈⠐⠀⠹⣿⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⡈⠀⢀⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢦⡈⠙⢦⣄⠈⠉⠉⠉⠉⠒⠊⠓⠚⠓⠛⢳⢒⣒⠦⣤⣤⣄⣠⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠻⣷⣶⣶⣤⣄⣀⣠⣤⣶⣦⣄⡀⠀⠀⠠⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠴⡄⢚⡔⠤⡄⠦⡜⣿⢩⢿⣿⡄⢃⡀⠃⠄⠀⠐⠠⠀⠂⠀⠄⢀⠠⠐⡀⠀⢀⣶⣾⣷⣄⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠣⡀⠘⠻⣖⠚⠛⠛⠛⠛⠙⠛⠛⠛⠋⠛⠉⠛⠉⠙⠉⠛⠙⠛⠛⠿⣟⠒⠲⠆⠐⠢⠐⡄⠢⢄⠢⠄⠤⢠⢀⠄⡀⢄⡀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣦⣬⣭⣙⣛⣻⣿⣿⣽⣹⣻⣿⣷⣦⣄⡀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠢⠍⠶⣎⢧⡝⢣⠗⣼⣏⣾⣿⡇⠂⡌⠱⣈⠂⠡⠄⢂⠡⠐⠠⠀⡐⠠⠡⢠⣿⣿⣿⡿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠂⠀⠈⠳⣄⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣄⡀⠂⡀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠈⠁⠈⠀⠑⠃⠈⠉⠱⠈⠅⢒⠂⠆⠤⠤⣀⠄⣀⡀⣀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣍⡉⠉⠉⠉⠙⠛⠿⢿⣿⣿⣻⢿⣿⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠈⡇⠹⡌⢛⠌⣇⡋⠾⢸⣿⣿⣧⠁⡌⢡⠀⡌⠁⠌⡀⠂⠄⡑⠀⡱⢀⠡⣾⣿⠋⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⣀⣀⣀⣀⣄⣄⣠⣠⣀⣠⣀⣀⣀⣀⣀⣀⣀⣀⣁⠀⠈⠀⠀⠀⠀⠀⠀⠀⠉⠀⠁⠈⠁⠉⠐⠈⠂⠅⠂⠄⠠⠄⠠⢀⠄⡀⢀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⢾⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠱⠌⡱⡘⢌⠚⢤⠑⠢⣿⣿⣿⣿⠀⡇⠄⠒⠠⢁⠂⡐⠉⡐⠠⠁⡰⢀⢲⣿⠁⣼⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣄⣀⣀⠀⠀⠀⠈⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⡍⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠙⠋⠛⠛⠛⠛⠛⠛⠛⠛⣟⠛⠛⣛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠚⠒⠛⢷⡂⠂⠂⠄⠠⠀⠀⠀⠀⡀⢀⠈⠳⡝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠈⡔⢠⠣⢈⡜⠦⡈⢤⣹⣿⣿⣿⠤⣄⠉⢆⡁⢂⡐⠠⠁⠄⡁⠂⠅⢂⣿⠃⣼⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣬⠁⠀⠀⠈⠉⠉⠉⠛⠛⠛⠲⠶⠾⢷⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣄⣀⣀⣀⣀⣀⣀⣸⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⡀⣀⣀⣀⢀⣀⣀⣀⣀⣀⢹⡬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠰⢌⢢⢃⠬⢌⠧⣼⢋⣿⣿⣿⣿⢀⡏⣧⣢⠴⣀⡄⠱⢈⠂⡌⢁⡎⢘⡧⢰⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⢸⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⡿⢿⠿⠟⠟⠿⠛⠟⠻⠛⠟⠛⠛⠟⠻⢛⠉⠉⠣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⢿⣛⠛⠛⣛⣛⣛⣛⣛⣛⣻⣥⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣀⡋⢔⢪⠘⡌⢡⡏⠀⣿⣿⣿⣿⣆⣷⡿⣟⠿⠿⣭⣓⢶⣤⣐⢸⣇⣾⢃⣿⣿⣻⣿⣿⣻⣿⣿⣿⡇⢈⡐⢈⠀⡀⠀⡁⣸⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠁⠈⠀⠁⠀⠀⠤⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣤⠵⠬⠦⠽⠴⠿⠇⣸⣿⣿⣿⣿⣇⢻⢸⡌⢳⣦⡀⠈⠉⠛⠻⣿⡆⠉⢸⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⠀⢄⣢⣄⣀⣐⠀⢯⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⠀⠀⡀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠈⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⡿⡟⠀⣻⣤⡘⠿⠂⡀⠀⠀⠈⢹⣶⣈⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⡇⢸⠀⣖⡬⢹⣇⠈⠄⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠒⠒⠒⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣀⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣤⢤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⡉⢐⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⡟⢀⠈⠳⢬⡙⠻⣷⣦⣄⠀⠀⠀⣸⢿⢿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣷⣌⣓⠺⠶⠞⠋⠄⢂⠈⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠶⣶⢶⣶⡶⠶⠶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣧⣴⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣤⠇⡸⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣷⣄⡁⠂⠙⠳⣤⣉⠻⢿⣶⣦⡇⠀⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠠⢤⣉⣉⠓⠶⠦⢴⡤⢦⣄⣀⣁⠈⠠⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣰⣿⣋⣉⠙⣄⣠⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣧⣿⣿⣿⢾⠃⠙⣯⢉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠟⠿
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣶⣶⣤⡙⠷⣦⣍⣻⠃⠸⡟⣹⠟⣿⣿⣿⣿⣿⣿⣿⣿⠐⠂⠤⢉⡉⢳⠒⠶⠤⣄⣈⡉⠙⠻⠷⣶⣦⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣁⠛⡁⠈⠁⠁⣻⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠟⠛⠛⠛⠋⠎⢈⠐⡾⠉⠉⠛⠙⠛⠛⠛⠛⠛⠛⠛⠶⠶⠶⠶⠶⠶⠴
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠫⠽⣿⣿⣿⣷⣶⣌⢻⡀⢸⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢘⠰⢀⠄⡀⠇⡀⠂⠄⡀⢉⡙⠓⣲⣤⣬⣭⣤⣈⣉⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠙⠛⠛⢛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡿⢿⡿⡿⠿⠿⠿⢿⣿⠿⢃⡀⢀⠀⡀⣀⣀⣀⣠⣀⣤⣠⣤⣠⣴⣠⣶⣤⣶⣴⣳⣾⣶⣧⢌⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠈⠛⠿⣿⣿⣧⣺⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⢠⠈⠔⠰⠀⢌⡁⢢⠐⡠⠰⣾⣿⣿⡿⠛⣉⠛⡙⠛⠛⠀⢀⠀⠀⣠⣴⣾⣿⣿⣿⣭⣴⣬⣬⣭⣭⣬⣤⣤⣤⣴⣴⣦⣤⣤⣴⣤⣴⣤⣦⣴⣤⣦⣴⣴⣶⣶⣷⡿⠿⣿⣾⣵⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⡟⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠈⠙⠿⣿⡳⢸⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣧⡘⠠⠉⢆⠡⢌⠠⣀⢃⠲⢀⣿⣿⣿⡿⢡⠘⠄⠒⡀⢂⠄⠨⠄⢊⣴⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡁⢀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠞⣿⣿⣿⣿⣿⣹⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⠸⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⡿⠀⠉⠹⢷⣈⡰⠈⠰⢀⠎⡰⢇⠹⣿⡿⠁⢰⠈⡈⠁⡆⢁⠸⣀⠏⠰⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣹⣿⣿⠷⡿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠉⠙⠓⠶⠦⣥⣚⣧⣷⢶⡦⣄⣰⢦⣅⡘⠤⠣⢔⡈⣷⣿⣿⣿⣶⣦⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠱⠈⠀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⡾⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣄⠈⣳⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠿⠿⠶⢶⣿⣁⣃⣠⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣥⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣯⡁⠃⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠚⠻⢿⣿⢿⢿⣿⣿⣛⣛⣛⣛⣛⡛⠿⠿⠿⠿⠟⠓⠚⠋⠉⠉⢁⡁⢾⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠜⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠿⠟⠟⠿⠷⠤⢼⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠟⡍⢫⠉⠉⠉⠉⠁⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠋⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠈⠛⠛⠚⠛⠛⠛⠛⠛⠋⠛⠉⠉⠉⠉⠉⠁⠉⠉⠀⠀⠀⠀⢱⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⣤⡾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⢿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣀⣀⣀⣀⣀⣠⣇⣀⣳⣀⣀⣠⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣿⣾⣿⣿⣟⣛⣋⠉⠉⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠂⠐⡈⢒⠙⡛⢻⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣠⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣼⣷⣶⣶⣶⣶⣶⣶⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢶⣳⣌⣒⢂⠒⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠁⠸⠭⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢿⠿⢿⠻⢟⠻⡉⠏⢊⠔⠂⢀⡈⠄⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠙⠛⠻⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⢿⡿⢿⠿⡿⠿⠿⡟⢿⠻⠟⡿⡟⠿⡛⢟⠻⢛⠻⠙⠏⡛⠩⠙⠊⠑⠈⠐⠈⠈⠀⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⡁⡁⠀⠃⠉⠉⠉⠙⠃⠙⠩⠋⠹⠉⠛⡙⢋⠛⡙⠫⠛⠛⠹⠛⡙⠫⠛⠙⠛⡙⠋⠛⡙⠋⠛⠩⢋⠙⠉⠎⠉⢋⠡⡉⠂⠑⢀⢂⢈⠈⠀⠊⠀⠁⢈⢀⠉⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''',delay=0.0001)
    time.sleep(2)

    typewriter_centered(Fore.YELLOW + '''....Please wait....''', delay=0.0001)
    time.sleep(3)
    typewriter_centered(Fore.YELLOW + '''PRESS ANY KEY TO CONTINUE...''', delay=0.0001)
    input()


def main_menu(stdscr):
    """
    Menu principal façon 'PIT STOP' avec un banner ASCII,
    des options navigables au clavier et la possibilité de quitter avec ESC.
    Retourne le nom de l'option choisie ou None si ESC.
    """
    curses.curs_set(0)
    stdscr.nodelay(False)
    curses.start_color()

    # Paires de couleurs (à ajuster selon vos préférences)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Banner
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Options inactives
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Option sélectionnée
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Instructions

    # BANNIÈRE : soit vous utilisez pyfiglet, soit vous intégrez votre ASCII perso
    # Exemple avec pyfiglet :
    banner_text = pyfiglet.figlet_format("TYPING RACERS", font="slant")

    # Liste des options du menu
    options = [
        "Time Attack solo",
        "Grand Prix",
        "Mode Multijoueurs",
        "Tutoriel",
        "Quitter"
    ]
    current_option = 0  # Index de l'option sélectionnée

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # --- Afficher la bannière en haut, centrée ---
        banner_lines = banner_text.splitlines()
        for idx, line in enumerate(banner_lines):
            x = max(0, (w - len(line)) // 2)
            stdscr.addstr(idx, x, line, curses.color_pair(1) | curses.A_BOLD)

        # --- Afficher les options du menu ---
        menu_start = len(banner_lines) + 2
        for i, option in enumerate(options):
            # On met en surbrillance l'option sélectionnée
            if i == current_option:
                text = f"> {option} <"
                color = curses.color_pair(3) | curses.A_BOLD
            else:
                text = f"  {option}  "
                color = curses.color_pair(2)

            x = max(0, (w - len(text)) // 2)
            stdscr.addstr(menu_start + i, x, text, color)

        # --- Instructions en bas ---
        instructions = "Flèches haut/bas (ou j/k) pour naviguer, ENTER pour sélectionner, ESC pour quitter."
        stdscr.addstr(h - 2, 2, instructions, curses.color_pair(4))

        stdscr.refresh()

        # Lecture des touches
        key = stdscr.getch()

        # ESC pour quitter
        if key == 27:  # ESC
            return None
        elif key in (curses.KEY_UP, ord('k')):
            current_option = (current_option - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord('j')):
            current_option = (current_option + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            # ENTER pour valider
            return options[current_option]

def menu():
    """
    Menu principal « hors curses » : appelle main_menu() dans curses
    et lance la fonction appropriée selon le choix de l’utilisateur.
    """

    selected = curses.wrapper(main_menu)

    if selected is None:
        # L'utilisateur a appuyé sur ESC dans le menu
        return
    elif selected == "Time Attack solo":
        curses.wrapper(time_attack.main)  # Exemple : lance la fonction main() de time_attack
    elif selected == "Grand Prix":
        # À implémenter
        print("Grand Prix à venir !")
    elif selected == "Mode Multijoueurs":
        print("Grand Prix à venir !")
    elif selected == "Tutoriel":
        curses.wrapper(typing_racers)
    elif selected == "Quitter":
        # On sort tout simplement
        return
def main():
    maximize_console_window()
    intro()
    menu()

if __name__ == "__main__":
    main()
