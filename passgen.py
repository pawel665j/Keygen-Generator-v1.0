# passgen.py
import random
import string
from typing import List

SYMBOLS = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?"
EMAIL_DOMAINS = ["@gmail.com", "@outlook.com", "@yahoo.com", "@mail.ru", "@yandex.ru"]

# Словари для "умного" логина
COMMON_NAMES = [
    "user", "player", "gamer", "agent", "admin", "guest", "boss", "king", "queen",
    "star", "hero", "ninja", "wolf", "fox", "bear", "cat", "dog", "bird", "fish",
    "alpha", "beta", "omega", "zero", "prime", "shadow", "light", "dark", "nova"
]

COMMON_SUFFIXES = [
    "pro", "master", "king", "god", "one", "x", "elite", "vip", "max", "top", "fast"
]

POPULAR_NAMES = [
    "Alex", "Bob", "Alice", "Mike", "Kate", "John", "Luna", "Sam", "Tom", "Anna",
    "Max", "Leo", "Zoe", "Eva", "Dan", "Nina", "Tim", "Sara", "Roy", "Mia"
]

class PasswordGenerator:
    """
    Генератор паролей и логинов.
    Полностью совместим с UI: понимает "Случайно", gen_username, show_username, add_domain.
    """

    def __init__(self):
        pass

    def _get_char_set(self, use_digits: bool, use_upper: bool, use_lower: bool, use_symbols: bool) -> str:
        """Собирает строку доступных символов для пароля"""
        char_set = ""
        if use_digits: char_set += string.digits
        if use_upper: char_set += string.ascii_uppercase
        if use_lower: char_set += string.ascii_lowercase
        if use_symbols: char_set += SYMBOLS
        return char_set

    def generate_password(self, length: int = 12, use_digits: bool = True, use_upper: bool = True,
                          use_lower: bool = True, use_symbols: bool = True) -> str:
        """Генерация случайного пароля по длине и набору символов"""
        chars = self._get_char_set(use_digits, use_upper, use_lower, use_symbols)
        if not chars:
            raise ValueError("Нет доступных символов для пароля")
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_username(self, length: int = 8) -> str:
        """
        Генерация умного логина: читаемого, похожего на реального пользователя.
        Примеры: user123, Alex_k, Ninja2025, gamer_x
        """
        mode = random.choice(["word_number", "name_letter", "prefix", "underscore"])

        if mode == "word_number":
            word = random.choice(COMMON_NAMES)
            num = random.randint(0, 9999)
            candidate = f"{word}{num}"
            return candidate[:length] if len(candidate) > length else candidate

        elif mode == "name_letter":
            name = random.choice(POPULAR_NAMES)
            letter = random.choice(string.ascii_lowercase)
            separator = "_" if random.random() < 0.7 else ""
            candidate = f"{name}{separator}{letter}"
            return candidate[:length] if len(candidate) > length else candidate

        elif mode == "prefix":
            prefix = random.choice(["User", "Player", "Agent", "Guest"])
            num = random.randint(1, 9999)
            candidate = f"{prefix}{num}"
            return candidate[:length] if len(candidate) > length else candidate

        elif mode == "underscore":
            part1 = random.choice(COMMON_NAMES)
            part2 = random.choice(COMMON_SUFFIXES)
            candidate = f"{part1}_{part2}"
            return candidate[:length] if len(candidate) > length else candidate

        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_combined(self, mode: str = "password", count: int = 1, **kwargs) -> List[str]:
        """
        Гибкая генерация:
        - Поддерживает mode="Случайно", "По шаблону", "По образцу"
        - Использует gen_username, username_length, show_username, add_domain, domain
        - Возвращает login:pass, email:pass, только пароль и т.д.
        """
        results = []
        for _ in range(count):
            # Определяем, нужен ли логин
            need_username = kwargs.get("gen_username", False)
            username = self.generate_username(kwargs.get("username_length", 8)) if need_username else None

            # Генерируем пароль
            password = self.generate_password(
                length=kwargs.get("length", 12),
                use_digits=kwargs.get("use_digits", True),
                use_upper=kwargs.get("use_upper", True),
                use_lower=kwargs.get("use_lower", True),
                use_symbols=kwargs.get("use_symbols", True)
            )

            # Определяем, что показывать
            show_username = kwargs.get("show_username", True)
            add_domain = kwargs.get("add_domain", False)
            domain = kwargs.get("domain", "@gmail.com")

            # Формируем результат
            if need_username:
                base_user = username
                if add_domain:
                    base_user = f"{username}{domain}"
                if show_username:
                    result = f"{base_user}:{password}"
                else:
                    result = base_user
            else:
                result = password

            results.append(result)

        return results