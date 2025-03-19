#!/usr/bin/env python3
import curses
import time
import random
import pyfiglet

# Définition de l'ASCII car
CAR_ASCII = "ō͡≡o˞_"


def main_menu(stdscr):
    """
    Affiche le menu principal avec un banner ASCII "PIT STOP" et 4 options.
    Le joueur navigue avec les flèches et valide avec ENTER.
    ESC quitte le menu.
    """
    curses.curs_set(0)
    stdscr.nodelay(False)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Texte normal
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Pour erreurs
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Texte de base
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Option sélectionnée

    # Créer un banner ASCII avec pyfiglet pour le thème Pit Stop
    title_text = pyfiglet.figlet_format("PIT STOP", font="slant")

    # Options du menu
    options = ["3 Minutes", "5 Minutes", "10 Minutes", "Infini"]
    current_option = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Afficher le banner en haut et centré
        banner_lines = title_text.splitlines()
        for idx, line in enumerate(banner_lines):
            stdscr.addstr(idx, max(0, (width - len(line)) // 2), line, curses.color_pair(3))

        # Afficher les options du menu sous le banner
        menu_start = len(banner_lines) + 2
        for i, option in enumerate(options):
            if i == current_option:
                option_text = "> " + option + " <"
                stdscr.addstr(menu_start + i, max(0, (width - len(option_text)) // 2), option_text,
                              curses.color_pair(4))
            else:
                option_text = "  " + option + "  "
                stdscr.addstr(menu_start + i, max(0, (width - len(option_text)) // 2), option_text,
                              curses.color_pair(3))

        # Instructions en bas
        stdscr.addstr(height - 2, 2, "Flèches haut/bas pour naviguer, ENTER pour sélectionner, ESC pour quitter.",
                      curses.color_pair(3))
        stdscr.refresh()

        key = stdscr.getch()
        if key == 27:  # ESC
            return None
        elif key in (curses.KEY_UP, ord('k')):
            current_option = (current_option - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord('j')):
            current_option = (current_option + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            return options[current_option]


def time_attack_mode(stdscr, mode):
    """
    Mode Time Attack dans lequel le joueur doit taper des phrases successivement.
    Pour les modes 3, 5, 10 minutes, un compte à rebours est affiché.
    Pour "Infini", le temps écoulé est affiché.
    ESC permet de quitter à tout moment.
    """
    # Durée en secondes selon le mode
    if mode == "3 Minutes":
        time_limit = 3 * 60
    elif mode == "5 Minutes":
        time_limit = 5 * 60
    elif mode == "10 Minutes":
        time_limit = 10 * 60
    elif mode == "Infini":
        time_limit = None  # Mode infini
    else:
        time_limit = None

    # Configuration de curses
    curses.curs_set(0)
    stdscr.nodelay(True)  # lecture non bloquante
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Texte correct
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Erreurs
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Texte de base
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Piste et ASCII art
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Statistiques

    # Banner pour le mode Time Attack
    banner_text = pyfiglet.figlet_format("TIME ATTACK", font="digital")

    # Dictionnaire de phrases à taper
    texts = [
    "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre. (Albert Einstein)",
    "L'imagination est plus importante que le savoir. (Albert Einstein)",
    "Tout ce que je sais, c'est que je ne sais rien. (Socrate)",
    "La vie est une fleur, l'amour en est le miel. (Victor Hugo)",
    "La simplicité est la sophistication suprême. (Léonard de Vinci)",
    "Soyez vous-même, tous les autres sont déjà pris. (Oscar Wilde)",
    "La seule chose que nous ayons à craindre, c'est la peur elle-même. (Franklin D. Roosevelt)",
    "Je pense, donc je suis. (René Descartes)",
    "Le futur appartient à ceux qui croient en la beauté de leurs rêves. (Eleanor Roosevelt)",
    "La liberté commence où l'ignorance finit. (Victor Hugo)",
    "Rien ne sert de courir, il faut partir à point. (Jean de La Fontaine)",
    "Le succès, c'est aller d'échec en échec sans perdre son enthousiasme. (Winston Churchill)",
    "La simplicité est la sophistication suprême. (Léonard de Vinci)",
    "N'attends pas que les événements arrivent comme tu le souhaites ; décide de vouloir ce qui arrive. (Épictète)",
    "Se tromper est humain, persévérer est diabolique. (Sénèque)",
    "La vérité est rarement pure et jamais simple. (Oscar Wilde)",
    "Rien de grand ne s'est accompli dans le monde sans passion. (Hegel)",
    "L'homme est condamné à être libre. (Jean-Paul Sartre)",
    "Celui qui déplace une montagne commence par déplacer de petites pierres. (Confucius)",
    "La meilleure façon de prédire l'avenir, c'est de le créer. (Peter Drucker)",
    "Il n'y a point de génie sans un grain de folie. (Aristote)",
    "Le doute est le commencement de la sagesse. (Aristote)",
    "On ne voit bien qu'avec le cœur, l'essentiel est invisible pour les yeux. (Antoine de Saint-Exupéry)",
    "L'éducation est l'arme la plus puissante pour changer le monde. (Nelson Mandela)",
    "La logique vous mènera d'un point A à un point B. L'imagination vous mènera partout. (Albert Einstein)",
    "Le courage n'est pas l'absence de peur, mais la capacité de vaincre ce qui fait peur. (Nelson Mandela)",
    "Connais-toi toi-même. (Inscription du temple de Delphes)",
    "La vie est un mystère qu'il faut vivre, et non un problème à résoudre. (Gandhi)",
    "On ne voit bien qu'avec le cœur, l'essentiel est invisible pour les yeux. (Antoine de Saint-Exupéry)",
    "Un voyage de mille lieues commence toujours par un premier pas. (Lao Tseu)",
    "La connaissance s'acquiert par l'expérience, tout le reste n'est que de l'information. (Albert Einstein)",
    "Le temps perdu ne se rattrape jamais. (Benjamin Franklin)",
    "Être ou ne pas être, telle est la question. (William Shakespeare)",
    "Celui qui sait écouter deviendra celui qu'on écoute. (Proverbe arabe)",
    "Connais-toi toi-même. (Platon)",
    "Le bonheur est parfois caché dans l'inconnu. (Victor Hugo)",
    "Rien de grand ne s'est accompli sans passion. (Hegel)",
    "Ne jugez pas chaque jour à la récolte que vous faites, mais aux graines que vous plantez. (Robert Louis Stevenson)",
    "Ce qui ne tue pas rend plus fort. (Friedrich Nietzsche)",
    "Tout est difficile avant d’être facile. (Thomas Fuller)",
    "Faites toujours ce que vous avez peur de faire. (Ralph Waldo Emerson)",
    "Être libre, ce n'est pas pouvoir faire ce que l'on veut, mais vouloir ce que l'on peut. (Jean-Paul Sartre)",
    "La seule chose constante, c’est le changement. (Héraclite)",
    "Le temps est ce que nous désirons le plus, mais que nous utilisons le moins bien. (William Penn)",
    "Ce n’est pas la force, mais la persévérance, qui fait les grandes œuvres. (Samuel Johnson)",
    "Le doute est le commencement de la sagesse. (Aristote)",
    "Le vrai bonheur consiste à faire des heureux. (Stanilas Leszczynski)",
    "Si vous pensez que l’aventure est dangereuse, essayez la routine, elle est mortelle. (Paulo Coelho)",
    "C’est justement la possibilité de réaliser un rêve qui rend la vie intéressante. (Paulo Coelho)",
    "Tout ce que tu peux imaginer est réel. (Pablo Picasso)",
    "Si tu veux aller vite, marche seul, mais si tu veux aller loin, marchons ensemble. (Proverbe africain)",
    "Une erreur originale vaut mieux qu'une vérité banale. (Fiodor Dostoïevski)",
    "La vérité attend. Seul le mensonge est pressé. (Alexandre Soljenitsyne)",
    "La vie est faite de petites victoires, remportées jour après jour. (Louise Hay)",
    "La simplicité est la clé du véritable succès. (Bruce Lee)",
    "Il est dur d’échouer, mais il est pire de n’avoir jamais tenté. (Theodore Roosevelt)",
    "Votre temps est limité, ne le gâchez pas à vivre la vie de quelqu’un d’autre. (Steve Jobs)",
    "Soyez vous-même, les autres sont déjà pris. (Oscar Wilde)",
    "Rien n’est permanent, sauf le changement. (Héraclite)",
    "Il vaut mieux viser la perfection et la manquer, que viser la médiocrité et l’atteindre. (Francis Blanche)",
    "C’est en faisant des erreurs qu’on apprend. (Proverbe français)",
    "La vie est faite de choix : Oui ou non, continuer ou abandonner, aimer ou ignorer. (Charles Bukowski)"


    ]
    current_phrase = random.choice(texts)
    typed_text = []  # Texte saisi pour la phrase en cours

    # Statistiques cumulées
    total_inputs = 0
    correct_inputs = 0
    phrases_completed = 0

    track_length = 50
    start_time = time.time()

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        current_time = time.time()
        elapsed = current_time - start_time

        if time_limit is not None:
            remaining = max(0, time_limit - elapsed)
        else:
            remaining = elapsed  # Mode infini affiche le temps écoulé

        # Fin du mode si le temps est écoulé (pour les modes limités)
        if time_limit is not None and remaining <= 0:
            game_over = True
        else:
            game_over = False

        # Calcul du nombre de caractères corrects consécutifs pour la phrase courante
        typed_index = 0
        for i, ch in enumerate(typed_text):
            if i < len(current_phrase) and ch == current_phrase[i]:
                typed_index += 1
            else:
                break

        # Vérification : si la phrase est entièrement et correctement tapée,
        # on considère la course réussie pour cette phrase.
        if typed_index == len(current_phrase):
            phrases_completed += 1
            stdscr.addstr(height // 2, max(0, (width - 30) // 2), "FÉLICITATIONS !", curses.color_pair(1))
            stdscr.refresh()
            time.sleep(1)  # Pause avant de passer à la phrase suivante
            current_phrase = random.choice(texts)  # Nouvelle phrase
            typed_text = []  # Réinitialisation du texte saisi
            continue

        # Calcul des statistiques cumulées
        accuracy = (correct_inputs / total_inputs * 100) if total_inputs > 0 else 0
        cpm = (correct_inputs / elapsed * 60) if elapsed > 0 else 0

        # Affichage du banner TIME ATTACK
        banner_lines = banner_text.splitlines()
        for idx, line in enumerate(banner_lines):
            stdscr.addstr(idx, max(0, (width - len(line)) // 2), line, curses.color_pair(3))

        # Affichage du timer
        if time_limit is not None:
            mins = int(remaining) // 60
            secs = int(remaining) % 60
            timer_str = f"Temps restant : {mins:02d}:{secs:02d}"
        else:
            mins = int(remaining) // 60
            secs = int(remaining) % 60
            timer_str = f"Temps écoulé : {mins:02d}:{secs:02d}"
        stdscr.addstr(len(banner_lines) + 1, 2, timer_str, curses.color_pair(5))

        # Affichage de la phrase à taper
        stdscr.addstr(len(banner_lines) + 3, 2, "Texte à taper :", curses.color_pair(3))
        stdscr.addstr(len(banner_lines) + 4, 2, current_phrase, curses.color_pair(3))

        # Affichage du texte saisi (avec coloration)
        stdscr.addstr(len(banner_lines) + 6, 2, "Texte saisi :", curses.color_pair(3))
        for i, ch in enumerate(typed_text):
            if i < len(current_phrase) and ch == current_phrase[i]:
                stdscr.addstr(len(banner_lines) + 7, 2 + i, ch, curses.color_pair(1))
            else:
                stdscr.addstr(len(banner_lines) + 7, 2 + i, ch, curses.color_pair(2))

        # Dessiner la piste avec la voiture
        progress_ratio = typed_index / len(current_phrase) if current_phrase else 0
        car_position = int(progress_ratio * track_length)
        track_line = "[" + " " * car_position + CAR_ASCII + " " * max(track_length - car_position, 0) + "] FINISH"
        stdscr.addstr(len(banner_lines) + 9, 2, track_line, curses.color_pair(4))

        # Affichage des statistiques en temps réel
        stats_str = f"Accuracy: {accuracy:.2f}% | CPM: {cpm:.1f} | Phrases complétées: {phrases_completed}"
        stdscr.addstr(len(banner_lines) + 11, 2, stats_str, curses.color_pair(5))

        # Instructions
        stdscr.addstr(height - 2, 2, "ESC pour quitter à tout moment.", curses.color_pair(3))
        stdscr.refresh()

        # Gestion de l'entrée utilisateur
        try:
            key = stdscr.getch()
        except:
            key = -1

        if key == 27:  # ESC
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if typed_text:
                typed_text.pop()
        elif key != -1:
            try:
                ch = chr(key)
            except ValueError:
                ch = ''
            if ch:
                total_inputs += 1
                pos = len(typed_text)
                if pos < len(current_phrase) and ch == current_phrase[pos]:
                    correct_inputs += 1
                typed_text.append(ch)

        if game_over:
            break

        time.sleep(0.01)

    # Écran de fin
    stdscr.nodelay(False)
    stdscr.clear()
    end_msg = "Temps écoulé !" if time_limit is not None else "Fin de la course !"
    stdscr.addstr(height // 2 - 1, max(0, (width - 20) // 2), end_msg, curses.color_pair(3))
    final_stats = f"Final Accuracy: {accuracy:.2f}% | Final CPM: {cpm:.1f} | Phrases complétées: {phrases_completed}"
    stdscr.addstr(height // 2, max(0, (width - len(final_stats)) // 2), final_stats, curses.color_pair(3))
    stdscr.addstr(height // 2 + 2, max(0, (width - 40) // 2), "Appuyez sur une touche pour retourner au menu.",
                  curses.color_pair(3))
    stdscr.refresh()
    stdscr.getch()


def main(stdscr):
    """
    Boucle principale : affichage du menu puis lancement du mode sélectionné.
    """
    while True:
        option = main_menu(stdscr)
        if option is None:
            break  # ESC dans le menu
        time_attack_mode(stdscr, option)


if __name__ == "__main__":
    curses.wrapper(main)
