import random
from tabulate import tabulate
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

# Массивы для мастей и рангов карт
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['H', 'D', 'C', 'S']

# Генерируем колоду
def generate_deck(exclude_cards):
    deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
    return [card for card in deck if card not in exclude_cards]

# Функция для подсчета аутов
def count_outs(hand, board):
    full_hand = hand + board
    outs = 0
    deck = generate_deck(full_hand)

    rank_count = {rank: 0 for rank in ranks}
    for card in full_hand:
        rank = card[:-1]
        rank_count[rank] += 1
    
    for card in deck:
        rank = card[:-1]
        if rank_count[rank] == 1:
            outs += 2
        elif rank_count[rank] == 2:
            outs += 1

    return outs

# Функция для вычисления вероятности на победу
def calculate_win_probability(outs, remaining_cards):
    return (outs / remaining_cards) * 100 if remaining_cards > 0 else 0

# Функция для запроса карт у пользователя
def get_cards(prompt):
    print(prompt)
    cards = []
    for i in range(2):
        card = input(f"Карта {i + 1} (например, 'KH' для короля червей): ").strip().upper()
        if len(card) < 2 or card[:-1] not in ranks or card[-1] not in suits:
            print(Fore.RED + "Неправильный формат карты! Попробуйте еще раз.")
            return get_cards(prompt)
        cards.append(card)
    return cards

# Функция для ввода карт на флопе/терне/ривере
def get_board(prompt, num_cards):
    print(prompt)
    cards = []
    for i in range(num_cards):
        card = input(f"Карта {i + 1} (например, 'KH' для короля червей): ").strip().upper()
        if len(card) < 2 or card[:-1] not in ranks or card[-1] not in suits:
            print(Fore.RED + "Неправильный формат карты! Попробуйте еще раз.")
            return get_board(prompt, num_cards)
        cards.append(card)
    return cards

# Функция для отображения шпаргалки
def show_cheat_sheet():
    suits = {
        '\u2660': 'Spades',
        '\u2665': 'Hearts',
        '\u2666': 'Diamonds',
        '\u2663': 'Clubs'
    }
    print(Fore.GREEN + "Poker Suits Cheat Sheet:")
    cheat_sheet = [[symbol, name] for symbol, name in suits.items()]
    print(tabulate(cheat_sheet, headers=["Symbol", "Suit"], tablefmt="grid"))

# Основной скрипт
def main():
    while True:
        show_cheat_sheet()

        # Ввод карт игрока
        player_hand = get_cards(Fore.YELLOW + "Введите ваши две карты (например: 'KH' и 'QD'): ")
        
        # Количество карт, которые остаются в колоде до флопа
        remaining_cards = 52 - len(player_hand)

        # Подсчет аутов до флопа
        preflop_outs = count_outs(player_hand, [])
        preflop_win_percentage = calculate_win_probability(preflop_outs, remaining_cards)
        print(Fore.CYAN + f"\n{'-' * 40}\n"
              f"До флопа:\n"
              f"У вас {preflop_outs} аутов. Шанс на победу: {preflop_win_percentage:.2f}%\n"
              f"{'-' * 40}")

        # Ввод карт флопа
        show_cheat_sheet()
        flop = get_board(Fore.YELLOW + "Введите три карты на флопе:", 3)
        remaining_cards -= 3

        # Подсчет аутов после флопа
        flop_outs = count_outs(player_hand, flop)
        flop_win_percentage = calculate_win_probability(flop_outs, remaining_cards)
        print(Fore.CYAN + f"\n{'-' * 40}\n"
              f"После флопа:\n"
              f"У вас {flop_outs} аутов. Шанс на победу: {flop_win_percentage:.2f}%\n"
              f"{'-' * 40}")

        # Ввод карты терна
        show_cheat_sheet()
        turn = get_board(Fore.YELLOW + "Введите карту на терне:", 1)
        remaining_cards -= 1

        # Подсчет аутов после терна
        turn_outs = count_outs(player_hand, flop + turn)
        turn_win_percentage = calculate_win_probability(turn_outs, remaining_cards)
        print(Fore.CYAN + f"\n{'-' * 40}\n"
              f"После терна:\n"
              f"У вас {turn_outs} аутов. Шанс на победу: {turn_win_percentage:.2f}%\n"
              f"{'-' * 40}")

        # Ввод карты ривера
        show_cheat_sheet()
        river = get_board(Fore.YELLOW + "Введите карту на ривере:", 1)
        remaining_cards -= 1

        # Подсчет аутов после ривера
        river_outs = count_outs(player_hand, flop + turn + river)
        river_win_percentage = calculate_win_probability(river_outs, remaining_cards)
        print(Fore.CYAN + f"\n{'-' * 40}\n"
              f"После ривера:\n"
              f"У вас {river_outs} аутов. Шанс на победу: {river_win_percentage:.2f}%\n"
              f"{'-' * 40}")

        # Спрашиваем, хотят ли они сыграть еще раз
        play_again = input(Fore.YELLOW + "Хотите сыграть еще раз? (да/нет): ").strip().lower()
        if play_again != 'да':
            break

if __name__ == "__main__":
    main()
