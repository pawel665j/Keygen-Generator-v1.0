# keygen.py - Версия с продвинутой логикой
import random
import string
import re
from typing import List, Dict, Tuple
from collections import Counter, defaultdict
import statistics

SYMBOLS = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?"

class KeyGenerator:
    """
    Мощный генератор серийных ключей с продвинутой аналитикой.
    """
    
    def __init__(self):
        self.chars = {
            'X': string.digits,
            'Y': string.ascii_uppercase,
            'y': string.ascii_lowercase,
            'Z': SYMBOLS
        }

    def _get_char_set(self, use_digits: bool, use_upper: bool, use_lower: bool, use_symbols: bool) -> dict:
        """Фильтрует доступные наборы символов"""
        return {
            'X': self.chars['X'] if use_digits else '',
            'Y': self.chars['Y'] if use_upper else '',
            'y': self.chars['y'] if use_lower else '',
            'Z': self.chars['Z'] if use_symbols else ''
        }

    def generate_random(self, length: int, use_digits: bool = True, use_upper: bool = True,
                        use_lower: bool = False, use_symbols: bool = False) -> str:
        """Случайная генерация ключа заданной длины"""
        char_set = ''.join(self._get_char_set(use_digits, use_upper, use_lower, use_symbols).values())
        if not char_set:
            raise ValueError("Нет доступных символов для генерации")
        return ''.join(random.choice(char_set) for _ in range(length))

    def generate_from_pattern(self, pattern: str, use_digits: bool = True, use_upper: bool = True,
                              use_lower: bool = False, use_symbols: bool = False) -> str:
        """Генерация по шаблону: XXXX-YYYY → 1234-ABCD"""
        char_set = self._get_char_set(use_digits, use_upper, use_lower, use_symbols)
        result = []
        for char in pattern:
            if char in char_set and char_set[char]:
                result.append(random.choice(char_set[char]))
            else:
                result.append(char)  # Сохраняем разделители как есть
        return ''.join(result)

    def analyze_pattern(self, sample: str) -> str:
        """Определяет шаблон из примера: ABC-123 → YYY-XXX"""
        pattern = []
        for char in sample:
            if char.isdigit():
                pattern.append('X')
            elif char.isupper():
                pattern.append('Y')
            elif char.islower():
                pattern.append('y')
            elif char in SYMBOLS:
                pattern.append('Z')
            else:
                pattern.append(char)  # Сохраняем разделители
        return ''.join(pattern)

    def advanced_pattern_analysis(self, samples: List[str]) -> Dict:
        """
        Продвинутый анализ образцов:
        - Анализ структуры (длины сегментов)
        - Частотный анализ символов
        - Определение паттернов повторений
        - Статистический анализ
        """
        if not samples:
            return self._get_default_config()
        
        # Очистка и фильтрация образцов
        clean_samples = [s.strip() for s in samples if s.strip()]
        if not clean_samples:
            return self._get_default_config()
        
        # 1. Анализ структуры
        structure_analysis = self._analyze_structure(clean_samples)
        
        # 2. Анализ типов символов
        char_type_analysis = self._analyze_char_types_advanced(clean_samples)
        
        # 3. Анализ разделителей
        separator_analysis = self._analyze_separators(clean_samples)
        
        # 4. Определение подходящего режима
        mode_config = self._determine_generation_mode(
            structure_analysis, 
            char_type_analysis, 
            separator_analysis
        )
        
        return mode_config

    def _analyze_structure(self, samples: List[str]) -> Dict:
        """Анализ структуры образцов"""
        lengths = [len(sample) for sample in samples]
        
        # Анализ сегментов (разделенных не-буквами/не-цифрами)
        segments_info = []
        for sample in samples:
            # Разбиваем на сегменты по разделителям
            segments = re.split(r'[^a-zA-Z0-9]', sample)
            segments = [seg for seg in segments if seg]  # Убираем пустые
            segments_info.append({
                'count': len(segments),
                'lengths': [len(seg) for seg in segments],
                'segments': segments
            })
        
        return {
            'avg_length': statistics.mean(lengths) if lengths else 0,
            'min_length': min(lengths) if lengths else 0,
            'max_length': max(lengths) if lengths else 0,
            'std_length': statistics.stdev(lengths) if len(lengths) > 1 else 0,
            'segments_info': segments_info
        }

    def _analyze_char_types_advanced(self, samples: List[str]) -> Dict:
        """Продвинутый анализ типов символов"""
        all_text = ''.join(samples)
        
        # Подсчет частот
        digit_chars = [c for c in all_text if c.isdigit()]
        upper_chars = [c for c in all_text if c.isupper()]
        lower_chars = [c for c in all_text if c.islower()]
        symbol_chars = [c for c in all_text if c in SYMBOLS]
        
        total_chars = len(all_text)
        
        return {
            'digits': {
                'used': len(digit_chars) > 0,
                'frequency': len(digit_chars) / total_chars if total_chars > 0 else 0,
                'chars': set(digit_chars)
            },
            'upper': {
                'used': len(upper_chars) > 0,
                'frequency': len(upper_chars) / total_chars if total_chars > 0 else 0,
                'chars': set(upper_chars)
            },
            'lower': {
                'used': len(lower_chars) > 0,
                'frequency': len(lower_chars) / total_chars if total_chars > 0 else 0,
                'chars': set(lower_chars)
            },
            'symbols': {
                'used': len(symbol_chars) > 0,
                'frequency': len(symbol_chars) / total_chars if total_chars > 0 else 0,
                'chars': set(symbol_chars)
            }
        }

    def _analyze_separators(self, samples: List[str]) -> Dict:
        """Анализ разделителей"""
        all_separators = []
        for sample in samples:
            # Находим все не-алфанумерические символы
            separators = [c for c in sample if not c.isalnum()]
            all_separators.extend(separators)
        
        separator_counter = Counter(all_separators)
        most_common_separator = separator_counter.most_common(1)[0][0] if separator_counter else '-'
        
        return {
            'most_common': most_common_separator,
            'all_separators': list(set(all_separators)),
            'positions': self._analyze_separator_positions(samples)
        }

    def _analyze_separator_positions(self, samples: List[str]) -> Dict:
        """Анализ позиций разделителей"""
        position_data = defaultdict(list)
        
        for sample in samples:
            for i, char in enumerate(sample):
                if not char.isalnum():
                    position_data[i].append(char)
        
        # Находим наиболее частые позиции разделителей
        separator_positions = {}
        for pos, chars in position_data.items():
            most_common_char = Counter(chars).most_common(1)[0][0]
            separator_positions[pos] = most_common_char
            
        return separator_positions

    def _determine_generation_mode(self, structure: Dict, char_types: Dict, separators: Dict) -> Dict:
        """Определение оптимального режима генерации"""
        
        # Если есть четкая структура сегментов
        if structure['segments_info']:
            segments_consistent = self._check_segments_consistency(structure['segments_info'])
            if segments_consistent:
                return self._create_segmented_config(structure, char_types, separators)
        
        # Если образцы разной длины - случайная генерация с диапазоном
        if structure['std_length'] > 2:  # Большая вариация длины
            return self._create_variable_length_config(structure, char_types)
        
        # По умолчанию - анализ первого образца
        return self._create_simple_pattern_config(structure, char_types)

    def _check_segments_consistency(self, segments_info: List[Dict]) -> bool:
        """Проверка консистентности сегментов"""
        if len(segments_info) < 2:
            return True
            
        first_segment_count = segments_info[0]['count']
        return all(info['count'] == first_segment_count for info in segments_info)

    def _create_segmented_config(self, structure: Dict, char_types: Dict, separators: Dict) -> Dict:
        """Создание конфигурации для сегментированной структуры"""
        # Берем первый образец для анализа структуры
        if structure['segments_info']:
            first_sample_segments = structure['segments_info'][0]['segments']
            
            # Создаем шаблон для каждого сегмента
            segment_patterns = []
            for segment in first_sample_segments:
                pattern = self.analyze_pattern(segment)
                segment_patterns.append(pattern)
            
            # Создаем общий шаблон с разделителями
            # Для простоты используем наиболее частый разделитель
            separator = separators['most_common']
            full_pattern = separator.join(segment_patterns)
            
            return {
                'mode': 'pattern',
                'pattern': full_pattern,
                'use_digits': char_types['digits']['used'],
                'use_upper': char_types['upper']['used'],
                'use_lower': char_types['lower']['used'],
                'use_symbols': char_types['symbols']['used']
            }
        
        return self._get_default_config()

    def _create_variable_length_config(self, structure: Dict, char_types: Dict) -> Dict:
        """Создание конфигурации для переменной длины"""
        return {
            'mode': 'smart_random',
            'min_length': max(1, int(structure['min_length'])),
            'max_length': int(structure['max_length']),
            'use_digits': char_types['digits']['used'],
            'use_upper': char_types['upper']['used'],
            'use_lower': char_types['lower']['used'],
            'use_symbols': char_types['symbols']['used']
        }

    def _create_simple_pattern_config(self, structure: Dict, char_types: Dict) -> Dict:
        """Создание простой конфигурации по шаблону"""
        # Берем самый длинный образец для шаблона
        return {
            'mode': 'pattern',
            'pattern': 'X' * int(structure['max_length']),  # Простой шаблон
            'use_digits': char_types['digits']['used'],
            'use_upper': char_types['upper']['used'],
            'use_lower': char_types['lower']['used'],
            'use_symbols': char_types['symbols']['used']
        }

    def _get_default_config(self) -> Dict:
        """Конфигурация по умолчанию"""
        return {
            'mode': 'random',
            'length': 12,
            'use_digits': True,
            'use_upper': True,
            'use_lower': False,
            'use_symbols': False
        }

    def generate_smart_random(self, min_length: int, max_length: int, use_digits: bool = True,
                             use_upper: bool = True, use_lower: bool = False, 
                             use_symbols: bool = False) -> str:
        """Генерация ключа случайной длины в заданном диапазоне"""
        length = random.randint(min_length, max_length)
        return self.generate_random(length, use_digits, use_upper, use_lower, use_symbols)

    def generate_batch(self, count: int, mode: str, **kwargs) -> List[str]:
        """Генерация нескольких ключей"""
        results = []
        for _ in range(count):
            try:
                if mode == "random":
                    results.append(self.generate_random(**kwargs))
                elif mode == "pattern":
                    results.append(self.generate_from_pattern(**kwargs))
                elif mode == "from_sample":
                    sample = kwargs.pop("sample", "")
                    pattern = self.analyze_pattern(sample)
                    kwargs["pattern"] = pattern
                    results.append(self.generate_from_pattern(**kwargs))
                elif mode == "smart_random":
                    results.append(self.generate_smart_random(**kwargs))
                else:
                    results.append("Ошибка: неизвестный режим")
            except Exception as e:
                results.append(f"Ошибка: {str(e)}")
        return results