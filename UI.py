# UI8.py: Генератор ключей и паролей (Русский интерфейс) - Модульная архитектура
import dearpygui.dearpygui as dpg
import json
from keygen import KeyGenerator
from passgen import PasswordGenerator

# === Константы ===
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
EMAIL_DOMAINS = ["@gmail.com", "@outlook.com", "@yahoo.com", "@mail.ru", "@yandex.ru"]
DEFAULT_PATTERN = "XXXX-YYYY-ZZZZ"
FONT_PATH = "D:\\Keygen\\Fonts\\arial.ttf"
FONT_SIZE = 16

# === Глобальные переменные ===
key_generator = KeyGenerator()
password_generator = PasswordGenerator()
generated_results = []
generated_results_password = []
current_tab = "Keygen"

# === Инициализация DPG ===
dpg.create_context()

# === Регистрация шрифта с кириллицей ===
try:
    with dpg.font_registry():
        with dpg.font(FONT_PATH, FONT_SIZE) as font:
            dpg.add_font_chars(list(range(1040, 1104)) + [1025, 1105])
            dpg.bind_font(font)
except:
    print("Не удалось загрузить шрифт, использую системный")

def tab_changed_callback(sender, app_data):
    """Обработчик смены вкладки"""
    global current_tab
    if app_data == tab_password_id:
        current_tab = "Password"
    else:
        current_tab = "Keygen"
    print(f"Переключились на вкладку: {current_tab}")

def generate_handler():
    """Обработчик генерации"""
    global generated_results, generated_results_password, current_tab
    
    print(f"Текущая вкладка: {current_tab}")
    is_password = current_tab == "Password"

    if is_password:
        generate_passwords()
    else:
        generate_keys()

def generate_keys():
    """Генерация ключей через KeyGenerator"""
    global generated_results
    
    mode = dpg.get_value("gen_mode")
    count = dpg.get_value("count_input")
    use_digits = dpg.get_value("use_digits")
    use_upper = dpg.get_value("use_upper")
    use_lower = dpg.get_value("use_lower")
    use_symbols = dpg.get_value("use_symbols")
    length = dpg.get_value("length_input")
    pattern = dpg.get_value("pattern_input")
    sample = dpg.get_value("samples_input")
    separator = dpg.get_value("separator_input")

    try:
        if mode == "Случайно":
            results = key_generator.generate_batch(
                count=count,
                mode="random",
                length=length,
                use_digits=use_digits,
                use_upper=use_upper,
                use_lower=use_lower,
                use_symbols=use_symbols
            )
        elif mode == "По шаблону":
            results = key_generator.generate_batch(
                count=count,
                mode="pattern",
                pattern=pattern,
                use_digits=use_digits,
                use_upper=use_upper,
                use_lower=use_lower,
                use_symbols=use_symbols
            )
        elif mode == "По образцу":
            samples_text = sample.strip()
            if samples_text:
                # Разбиваем на отдельные образцы
                samples = [s.strip() for s in samples_text.split('\n') if s.strip()]
                if samples:
                    # Используем продвинутый анализ
                    smart_config = key_generator.advanced_pattern_analysis(samples)
                    
                    if smart_config['mode'] == 'pattern':
                        results = key_generator.generate_batch(
                            count=count,
                            mode="pattern",
                            pattern=smart_config['pattern'],
                            use_digits=smart_config['use_digits'],
                            use_upper=smart_config['use_upper'],
                            use_lower=smart_config['use_lower'],
                            use_symbols=smart_config['use_symbols']
                        )
                    elif smart_config['mode'] == 'smart_random':
                        results = key_generator.generate_batch(
                            count=count,
                            mode="smart_random",
                            min_length=smart_config['min_length'],
                            max_length=smart_config['max_length'],
                            use_digits=smart_config['use_digits'],
                            use_upper=smart_config['use_upper'],
                            use_lower=smart_config['use_lower'],
                            use_symbols=smart_config['use_symbols']
                        )
                    else:
                        # По умолчанию используем первый образец
                        first_sample = samples[0]
                        pattern = key_generator.analyze_pattern(first_sample)
                        results = key_generator.generate_batch(
                            count=count,
                            mode="pattern",
                            pattern=pattern,
                            use_digits=use_digits,
                            use_upper=use_upper,
                            use_lower=use_lower,
                            use_symbols=use_symbols
                        )
                else:
                    results = ["Ошибка: пустые образцы"]
            else:
                results = ["Ошибка: не указаны образцы"]
        else:
            results = ["Ошибка: неизвестный режим"]

        generated_results = results
        dpg.set_value("preview_output", "\n".join(results))
        print(f"Сгенерировано ключей: {len(results)}")
        
    except Exception as e:
        error_msg = f"Ошибка генерации: {str(e)}"
        dpg.set_value("preview_output", error_msg)
        print(error_msg)

def generate_passwords():
    """Генерация паролей через PasswordGenerator"""
    global generated_results_password
    
    mode = dpg.get_value("gen_mode_password")
    count = dpg.get_value("count_input_password")
    use_digits = dpg.get_value("use_digits_password")
    use_upper = dpg.get_value("use_upper_password")
    use_lower = dpg.get_value("use_lower_password")
    use_symbols = dpg.get_value("use_symbols_password")
    length = dpg.get_value("length_input_password")
    pattern = dpg.get_value("pattern_input_password")
    sample = dpg.get_value("samples_input_password")
    
    # Настройки логинов
    gen_username = dpg.get_value("gen_username")
    username_length = dpg.get_value("username_length")
    show_username = dpg.get_value("show_username")
    add_domain = dpg.get_value("add_domain")
    domain_select = dpg.get_value("domain_select")

    try:
        results = []
        for _ in range(count):
            # Генерируем пароль
            if mode == "Случайно":
                password = password_generator.generate_password(
                    length=length,
                    use_digits=use_digits,
                    use_upper=use_upper,
                    use_lower=use_lower,
                    use_symbols=use_symbols
                )
            elif mode == "По шаблону":
                # Для простоты используем обычную генерацию
                password = password_generator.generate_password(
                    length=length,
                    use_digits=use_digits,
                    use_upper=use_upper,
                    use_lower=use_lower,
                    use_symbols=use_symbols
                )
            elif mode == "По образцу":
                password = password_generator.generate_password(
                    length=length,
                    use_digits=use_digits,
                    use_upper=use_upper,
                    use_lower=use_lower,
                    use_symbols=use_symbols
                )
            else:
                password = "Ошибка"

            # Генерация логина/почты
            if gen_username:
                username = password_generator.generate_username(username_length)
                
                if add_domain:
                    if show_username:
                        result = f"{username}{domain_select}:   {password}"  
                    else:
                        result = f"{username}{domain_select}"
                else:
                    if show_username:
                        result = f"{username}:   {password}"  
                    else:
                        result = username
            else:
                result = password

            results.append(result)

        generated_results_password = results
        dpg.set_value("preview_output_password", "\n".join(results))
        print(f"Сгенерировано паролей: {len(results)}")
        
    except Exception as e:
        error_msg = f"Ошибка генерации: {str(e)}"
        dpg.set_value("preview_output_password", error_msg)
        print(error_msg)

def copy_to_clipboard():
    """Копирование в буфер обмена"""
    global generated_results, generated_results_password, current_tab
    if current_tab == "Password":
        if generated_results_password:
            dpg.set_clipboard_text("\n".join(generated_results_password))
    else:
        if generated_results:
            dpg.set_clipboard_text("\n".join(generated_results))

def save_to_file():
    """Сохранение в JSON"""
    global generated_results, generated_results_password, current_tab
    filename = "generated_passwords.json" if current_tab == "Password" else "generated_keys.json"
    data = generated_results_password if current_tab == "Password" else generated_results
    
    if data:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# === Создание UI ===
dpg.create_viewport(title="Генератор ключей и паролей", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

with dpg.window(label="Главное окно", width=WINDOW_WIDTH - 15, height=WINDOW_HEIGHT - 35):
    dpg.add_text("🔑 Генератор ключей и паролей", color=(0, 255, 255))
    dpg.add_spacer(height=10)

    with dpg.tab_bar(callback=tab_changed_callback):
        # ========= ВКЛАДКА: ГЕНЕРАТОР КЛЮЧЕЙ =========
        with dpg.tab(label="Генератор ключей", tag="Keygen") as tab_keygen_id:
            tab_keygen_id = dpg.last_item()
            with dpg.group(horizontal=True):
                with dpg.child_window(width=400):
                    dpg.add_text("⚙️ Настройки генерации", color=(0, 255, 0))
                    with dpg.collapsing_header(label="Режим генерации", default_open=True):
                        dpg.add_radio_button(
                            items=["Случайно", "По шаблону", "По образцу"],
                            default_value="Случайно",
                            tag="gen_mode"
                        )
                    with dpg.collapsing_header(label="Настройки символов", default_open=True):
                        dpg.add_input_int(label="Длина", default_value=12, min_value=2, max_value=1000, tag="length_input")
                        dpg.add_checkbox(label="Цифры (0-9)", default_value=True, tag="use_digits")
                        dpg.add_checkbox(label="Заглавные (A-Z)", default_value=True, tag="use_upper")
                        dpg.add_checkbox(label="Строчные (a-z)", default_value=False, tag="use_lower")
                        dpg.add_checkbox(label="Символы (!@#...)", default_value=False, tag="use_symbols")
                    with dpg.collapsing_header(label="Шаблон", default_open=False):
                        dpg.add_input_text(label="Формат", default_value=DEFAULT_PATTERN, tag="pattern_input")
                        dpg.add_input_text(label="Разделитель", default_value="-", width=50, tag="separator_input")
                    with dpg.collapsing_header(label="Анализ образцов", default_open=False):
                        dpg.add_input_text(multiline=True, height=100, tag="samples_input")
                    with dpg.collapsing_header(label="Вывод", default_open=True):
                        dpg.add_input_int(label="Количество", default_value=5, min_value=1, max_value=1000, tag="count_input")
                        dpg.add_button(label="Сгенерировать", callback=generate_handler, width=200, height=30)
                with dpg.child_window():
                    dpg.add_text("📋 Сгенерированные ключи", color=(0, 255, 0))
                    dpg.add_input_text(multiline=True, height=400, tag="preview_output", readonly=True)
                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Копировать", callback=copy_to_clipboard, width=150)
                        dpg.add_button(label="Сохранить в JSON", callback=save_to_file, width=150)

        # ========= ВКЛАДКА: ГЕНЕРАТОР ПАРОЛЕЙ =========
        with dpg.tab(label="Генератор паролей", tag="Password") as tab_password_id:
            tab_password_id = dpg.last_item()
            with dpg.group(horizontal=True):
                with dpg.child_window(width=400):
                    dpg.add_text("🔐 Настройки паролей", color=(0, 255, 0))
                    with dpg.collapsing_header(label="Настройки генерации", default_open=True):
                        dpg.add_radio_button(
                            items=["Случайно", "По шаблону", "По образцу"],
                            default_value="Случайно",
                            tag="gen_mode_password"
                        )
                        dpg.add_input_int(label="Длина", default_value=12, min_value=6, max_value=100, tag="length_input_password")
                        dpg.add_checkbox(label="Цифры (0-9)", default_value=True, tag="use_digits_password")
                        dpg.add_checkbox(label="Заглавные (A-Z)", default_value=True, tag="use_upper_password")
                        dpg.add_checkbox(label="Строчные (a-z)", default_value=True, tag="use_lower_password")
                        dpg.add_checkbox(label="Символы (!@#...)", default_value=True, tag="use_symbols_password")
                    with dpg.collapsing_header(label="Шаблон", default_open=False):
                        dpg.add_input_text(label="Формат", default_value="XXXXYYYYyyyyZZZZ", tag="pattern_input_password")
                    with dpg.collapsing_header(label="Анализ образцов", default_open=False):
                        dpg.add_input_text(multiline=True, height=100, tag="samples_input_password")
                    with dpg.collapsing_header(label="Логин / Email", default_open=True):
                        dpg.add_checkbox(label="Генерировать логин", default_value=False, tag="gen_username")
                        dpg.add_input_int(label="Длина логина", default_value=8, min_value=2, max_value=32, tag="username_length")
                        dpg.add_checkbox(label="Показывать с паролем", default_value=True, tag="show_username")
                        dpg.add_checkbox(label="Добавить домен", default_value=False, tag="add_domain")
                        dpg.add_combo(EMAIL_DOMAINS, default_value=EMAIL_DOMAINS[0], tag="domain_select")
                    with dpg.collapsing_header(label="Вывод", default_open=True):
                        dpg.add_input_int(label="Количество", default_value=5, min_value=1, max_value=100, tag="count_input_password")
                        dpg.add_button(label="Сгенерировать", callback=generate_handler, width=200, height=30)
                with dpg.child_window():
                    dpg.add_text("📋 Сгенерированные пароли", color=(0, 255, 0))
                    dpg.add_input_text(multiline=True, height=400, tag="preview_output_password", readonly=True)
                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Копировать", callback=copy_to_clipboard, width=150)
                        dpg.add_button(label="Сохранить в JSON", callback=save_to_file, width=150)

# === Запуск приложения ===
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()