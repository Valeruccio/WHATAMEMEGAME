import json
import os
import random
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox

try:
    import winsound
except ImportError:
    winsound = None


APP_TITLE = "Что за мем — менеджер игры"
SITUATIONS_FILE = "situations.json"
GREETINGS_FILE = "greetings.json"
REACTIONS_FILE = "reactions.json"

REACTION_BLOCKS = [
    "💀💀💀Стоп, время ставить КРУТЫХ скелетов💀💀💀",
    "🦴🦴🦴Стоп, время насыпать костей авторам🦴🦴🦴",
    "🤡🤡🤡Стоп, время навалить клоунам клоунов🤡🤡🤡",
    "🗿🗿🗿Стоп, засмеялся — проиграл, ставь реакции🗿🗿🗿",
    "🤢🤢🤢Стоп, время ливать из чатика или ставить реакции🤢🤢🤢",
    "🖤🖤🖤Стоп, не умер от кринжа? Ставь лойс!🖤🖤🖤",
    "🚬🚬🚬Стоп, помоги участникам выиграть, насыпь реакций🚬🚬🚬",
    "🔥🔥🔥Стоп, время ставить КРУТО🔥🔥🔥",
    "👍👍👍Стоп, время ставить КЛАССЫ👍👍👍",
    "🤙🤙🤙Стоп, время КУМАРА, ставьте лойсы🤙🤙🤙",
]


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_situations() -> list:
    path = resource_path(SITUATIONS_FILE)
    if not os.path.exists(path):
        default_situations = [
            {
                "id": 1,
                "text": "Когда решил произвести впечатление на собеседовании и демонстрируешь все свои навыки разом.",
                "theme": "работа",
            },
            {
                "id": 2,
                "text": "Когда руководитель придал тебе ускорения правильной мотивацией.",
                "theme": "работа",
            },
            {
                "id": 3,
                "text": "Отношу на помойку старую куртку. Бомж на следующий день…",
                "theme": "быт",
            },
            {
                "id": 4,
                "text": "Когда в день рождения банк списывает с карты все деньги в счет кредитной задолженности.",
                "theme": "деньги",
            },
            {
                "id": 5,
                "text": "Твое лицо, когда надо начинать работать, но сначала нужно подключить ВПН, а телефон с мультифактором разряжен.",
                "theme": "работа",
            },
            {
                "id": 6,
                "text": "Когда ИИ пытается забрать твою работу, но ты и не против.",
                "theme": "технологии",
            },
            {
                "id": 7,
                "text": "Когда в детстве стоишь на картонке в -20 и примеряешь новые штаны.",
                "theme": "детство",
            },
            {
                "id": 8,
                "text": "Проснулся от уведомлений рабочего чата, но там ругают не тебя.",
                "theme": "работа",
            },
            {
                "id": 9,
                "text": "Твое лицо, когда отпуск не дал должного результата.",
                "theme": "отдых",
            },
            {
                "id": 10,
                "text": "Последняя сохраненная картинка из твоей галереи в телефоне.",
                "theme": "рандом",
            },
            {
                "id": 11,
                "text": "Когда пообещал себе лечь спать в 23:00, а в 03:47 все еще листаешь мемы.",
                "theme": "сон",
            },
            {
                "id": 12,
                "text": "Когда на планерке спрашивают: \"Ну как там задачи?\", а ты только что открыл таск‑трекер.",
                "theme": "работа",
            },
            {
                "id": 13,
                "text": "Когда пытаешься объяснить родственникам, чем ты вообще занимаешься на своей работе.",
                "theme": "работа",
            },
            {
                "id": 14,
                "text": "Когда зашел в магазин за хлебом, а вышел с пакетом, полным того, что было по акции.",
                "theme": "деньги",
            },
            {
                "id": 15,
                "text": "Когда интернет завис ровно в тот момент, когда ты собирался быть продуктивным.",
                "theme": "технологии",
            },
            {
                "id": 16,
                "text": "Когда менеджер пишет \"Есть минутка?\" и пропадает на полчаса.",
                "theme": "работа",
            },
            {
                "id": 17,
                "text": "Когда ты уже попрощался на работе, надел куртку, а тебе говорят: \"О, как хорошо, что ты еще здесь\".",
                "theme": "работа",
            },
            {
                "id": 18,
                "text": "Когда решил поесть правильно, но на акции как раз твоя любимая шаурма.",
                "theme": "еда",
            },
            {
                "id": 19,
                "text": "Когда открыл банковское приложение после выходных.",
                "theme": "деньги",
            },
            {
                "id": 20,
                "text": "Когда добавил в календарь \"начать новую жизнь с понедельника\" и честно проигнорировал напоминание.",
                "theme": "саморазвитие",
            },
            {
                "id": 21,
                "text": "Когда написал в чат \"щас буду\" и через час еще даже не вышел из дома.",
                "theme": "опоздания",
            },
            {
                "id": 22,
                "text": "Когда коллега спросил \"а чё так долго?\", а ты два часа чинил его вчерашнюю инициативу.",
                "theme": "работа",
            },
            {
                "id": 23,
                "text": "Когда решил показать друзьям смешной мем, а пока искал, стало уже не смешно.",
                "theme": "мемы",
            },
            {
                "id": 24,
                "text": "Когда случайно включил фронталку и увидел себя настоящего.",
                "theme": "самоирония",
            },
            {
                "id": 25,
                "text": "Когда на корпоративе сказал лишнее, а на утро вспомнил, что это был не сон.",
                "theme": "корпоратив",
            },
            {
                "id": 26,
                "text": "Когда обещал себе не спорить в интернете, но кто‑то неправ.",
                "theme": "интернет",
            },
            {
                "id": 27,
                "text": "Когда поставил будильник на 7:00, но в 6:59 проснулся от мысли, что что‑то забыл.",
                "theme": "сон",
            },
            {
                "id": 28,
                "text": "Когда в зуме забыл выключить микрофон и начал комментировать происходящее.",
                "theme": "работа",
            },
            {
                "id": 29,
                "text": "Когда говоришь \"сейчас быстро отвечу на одно сообщение\" и пропадаешь в мессенджере на час.",
                "theme": "интернет",
            },
            {
                "id": 30,
                "text": "Когда после отпуска пришел на работу и понял, что пароль от компа помнишь лучше, чем ПИН от карты.",
                "theme": "работа",
            },
        ]
        save_situations(default_situations)
        return default_situations

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_situations(situations: list) -> None:
    path = resource_path(SITUATIONS_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(situations, f, ensure_ascii=False, indent=2)


def default_greetings() -> list[str]:
    base = (
        "💀 ПРИГОТОВЬТЕСЬ К ПРЫЖКУ В МЕМНУЮ ЯМУ 💀\n\n"
        "{start_time} | СИСТЕМА ЗАГРУЖЕНА | МОДЕРАТОР ПОДКЛЮЧЕН 🛰️💥\n\n"
        "Сегодня у нас игра «ЧТО ЗА МЕМ». Доставайте свои самые сочные сохры за неделю! 🦴🔥\n\n"
        "🕯️ ПРАВИЛА ИГРЫ:\n\n"
        "КВАРТАЛЬНЫЙ КЭШБЭК 💌 Твои реакции — твоя валюта и уважение. "
        "Набивай рейтинг, и раз в квартал Самый КРУТОЙ Автор получает реальный подгон.\n\n"
        "КИЛЛЕР МЕМПЛЕКС НЕДЕЛИ 💪 В конце считаем, у кого самый залайканный мем. "
        "Этот герой становится Победителем Недели.\n\n"
        "РЕАКТИВНЫЙ ТРИБУНАЛ ❌ Когда увидишь дескриптор «СТОП, ВРЕМЯ СТАВИТЬ ОЦЕНКИ», "
        "ставь реакции на те мемы, от которых у тебя вылетают диски из позвоночника.\n\n"
        "СКОРОСТНОЙ ПОНОС ИЗ МЕМОВ 🏎️💀 Я дропаю ситуацию — у тебя есть 3 минуты, "
        "чтобы выкинуть в чат мем. Не успел — тебя закибербулили! ⏰\n\n"
        "ПОГНАЛИ!\n"
    )
    return [base]


def load_greetings() -> list:
    path = resource_path(GREETINGS_FILE)
    if not os.path.exists(path):
        data = default_greetings()
        save_greetings(data)
        return data
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_greetings(greetings: list) -> None:
    path = resource_path(GREETINGS_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(greetings, f, ensure_ascii=False, indent=2)


def load_reactions() -> list:
    path = resource_path(REACTIONS_FILE)
    if not os.path.exists(path):
        save_reactions(REACTION_BLOCKS)
        return list(REACTION_BLOCKS)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_reactions(blocks: list) -> None:
    path = resource_path(REACTIONS_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(blocks, f, ensure_ascii=False, indent=2)


class TimerThread(threading.Thread):
    def __init__(self, seconds: int, on_tick, on_done):
        super().__init__(daemon=True)
        self.seconds = seconds
        self.on_tick = on_tick
        self.on_done = on_done
        self._stop_event = threading.Event()

    def run(self):
        remaining = self.seconds
        while remaining >= 0 and not self._stop_event.is_set():
            self.on_tick(remaining)
            time.sleep(1)
            remaining -= 1
        if not self._stop_event.is_set():
            self.on_done()

    def stop(self):
        self._stop_event.set()


class MemeGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x700")

        self.situations = load_situations()
        self.greetings = load_greetings()
        self.reactions = load_reactions()
        self.current_timer: TimerThread | None = None
        self.script_font: tkfont.Font | None = None
        self.situation_choice_to_index: dict[str, int] | None = None
        self.situation_select_vars: list[tk.StringVar] = []

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.situations_frame = ttk.Frame(notebook)
        self.greetings_frame = ttk.Frame(notebook)
        self.reactions_frame = ttk.Frame(notebook)
        self.script_frame = ttk.Frame(notebook)
        self.timer_frame = ttk.Frame(notebook)

        notebook.add(self.situations_frame, text="Банк ситуаций")
        notebook.add(self.greetings_frame, text="Приветствия")
        notebook.add(self.reactions_frame, text="STOP-реакции")
        notebook.add(self.script_frame, text="Программа игры")
        notebook.add(self.timer_frame, text="Таймер")

        self.init_situations_tab()
        self.init_greetings_tab()
        self.init_reactions_tab()
        self.init_script_tab()
        self.init_timer_tab()

    # --- Situations tab ---
    def init_situations_tab(self):
        left = ttk.Frame(self.situations_frame)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        right = ttk.Frame(self.situations_frame)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(left, text="Ситуации").pack(anchor="w")

        self.situations_list = tk.Listbox(left, width=45)
        self.situations_list.pack(fill=tk.BOTH, expand=True)
        self.situations_list.bind("<<ListboxSelect>>", self.on_situation_select)

        btns = ttk.Frame(left)
        btns.pack(fill=tk.X, pady=5)

        ttk.Button(btns, text="Добавить", command=self.add_situation).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(btns, text="Изменить", command=self.edit_situation).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(btns, text="Удалить", command=self.delete_situation).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(btns, text="Копировать", command=self.copy_situation_to_clipboard).pack(
            side=tk.LEFT, padx=2
        )

        ttk.Label(right, text="Текст ситуации:").pack(anchor="w")
        self.situation_text = tk.Text(right, height=6, wrap=tk.WORD)
        self.situation_text.pack(fill=tk.X)

        theme_frame = ttk.Frame(right)
        theme_frame.pack(fill=tk.X, pady=5)
        ttk.Label(theme_frame, text="Тема:").pack(side=tk.LEFT)
        self.situation_theme_var = tk.StringVar()
        self.situation_theme_entry = ttk.Entry(
            theme_frame, textvariable=self.situation_theme_var
        )
        self.situation_theme_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Button(
            right, text="Сохранить изменения", command=self.save_situation_changes
        ).pack(anchor="e", pady=5)

        self.refresh_situations_list()

    def refresh_situations_list(self):
        self.situations_list.delete(0, tk.END)
        for s in self.situations:
            label = f"{s.get('id', '')}. [{s.get('theme', '')}] {s.get('text', '')[:60]}..."
            self.situations_list.insert(tk.END, label)

    def get_selected_index(self):
        selection = self.situations_list.curselection()
        if not selection:
            return None
        return selection[0]

    def on_situation_select(self, _event=None):
        idx = self.get_selected_index()
        if idx is None:
            return
        s = self.situations[idx]
        self.situation_text.delete("1.0", tk.END)
        self.situation_text.insert("1.0", s.get("text", ""))
        self.situation_theme_var.set(s.get("theme", ""))

    def add_situation(self):
        new = {
            "id": max((s.get("id", 0) for s in self.situations), default=0) + 1,
            "text": "Новая ситуация...",
            "theme": "",
        }
        self.situations.append(new)
        save_situations(self.situations)
        self.refresh_situations_list()
        self.situations_list.selection_clear(0, tk.END)
        self.situations_list.selection_set(tk.END)
        self.on_situation_select()

    def edit_situation(self):
        if self.get_selected_index() is None:
            messagebox.showinfo("Редактирование", "Выберите ситуацию в списке.")
            return
        self.on_situation_select()

    def save_situation_changes(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Сохранение", "Выберите ситуацию для сохранения.")
            return
        self.situations[idx]["text"] = self.situation_text.get("1.0", tk.END).strip()
        self.situations[idx]["theme"] = self.situation_theme_var.get().strip()
        save_situations(self.situations)
        self.refresh_situations_list()

    def delete_situation(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        if not messagebox.askyesno(
            "Удалить", "Точно удалить выбранную ситуацию из банка?"
        ):
            return
        self.situations.pop(idx)
        save_situations(self.situations)
        self.refresh_situations_list()
        self.situation_text.delete("1.0", tk.END)
        self.situation_theme_var.set("")

    def copy_situation_to_clipboard(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Буфер обмена", "Выберите ситуацию для копирования.")
            return
        text = self.situations[idx]["text"]
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Скопировано", "Текст ситуации скопирован в буфер.")

    # --- Greetings tab ---
    def init_greetings_tab(self):
        frame = self.greetings_frame

        box = ttk.LabelFrame(frame, text="Банк приветствий")
        box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.greetings_list = tk.Listbox(box, height=8)
        self.greetings_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.greetings_list.bind("<<ListboxSelect>>", self.on_greeting_select)

        greet_btns = ttk.Frame(box)
        greet_btns.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(greet_btns, text="Добавить", command=self.add_greeting).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(greet_btns, text="Удалить", command=self.delete_greeting).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(
            greet_btns,
            text="Копировать",
            command=self.copy_greeting_to_clipboard,
        ).pack(side=tk.LEFT, padx=2)

        ttk.Label(box, text="Текст выбранного приветствия:").pack(
            anchor="w", padx=5
        )
        self.greeting_text = tk.Text(box, height=12, wrap=tk.WORD)
        self.greeting_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        ttk.Button(
            box, text="Сохранить изменения", command=self.save_greeting_changes
        ).pack(anchor="e", padx=5, pady=(0, 5))

        self.refresh_greetings_list()

    def refresh_greetings_list(self):
        self.greetings_list.delete(0, tk.END)
        for g in self.greetings:
            first_line = g.splitlines()[0] if g.splitlines() else g
            self.greetings_list.insert(tk.END, first_line[:80])

    def get_selected_greeting_index(self):
        selection = self.greetings_list.curselection()
        if not selection:
            return None
        return selection[0]

    def on_greeting_select(self, _event=None):
        idx = self.get_selected_greeting_index()
        if idx is None:
            return
        text = self.greetings[idx]
        self.greeting_text.delete("1.0", tk.END)
        self.greeting_text.insert("1.0", text)

    def add_greeting(self):
        tmpl = (
            "💀 ПРИГОТОВЬТЕСЬ К ПРЫЖКУ В МЕМНУЮ ЯМУ 💀\n\n"
            "{start_time} | СИСТЕМА ЗАГРУЖЕНА | МОДЕРАТОР ПОДКЛЮЧЕН 🛰️💥\n\n"
            "Новое кастомное приветствие.\n"
        )
        self.greetings.append(tmpl)
        save_greetings(self.greetings)
        self.refresh_greetings_list()
        self.greetings_list.selection_clear(0, tk.END)
        self.greetings_list.selection_set(tk.END)
        self.on_greeting_select()

    def save_greeting_changes(self):
        idx = self.get_selected_greeting_index()
        if idx is None:
            messagebox.showinfo("Приветствия", "Выберите приветствие для сохранения.")
            return
        text = self.greeting_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo(
                "Приветствия", "Текст приветствия не может быть пустым."
            )
            return
        self.greetings[idx] = text
        save_greetings(self.greetings)
        self.refresh_greetings_list()

    def delete_greeting(self):
        idx = self.get_selected_greeting_index()
        if idx is None:
            return
        if not messagebox.askyesno(
            "Приветствия", "Удалить выбранное приветствие из банка?"
        ):
            return
        self.greetings.pop(idx)
        if not self.greetings:
            self.greetings = default_greetings()
        save_greetings(self.greetings)
        self.refresh_greetings_list()
        self.greeting_text.delete("1.0", tk.END)

    def copy_greeting_to_clipboard(self):
        idx = self.get_selected_greeting_index()
        if idx is None:
            messagebox.showinfo("Приветствия", "Выберите приветствие для копирования.")
            return
        text = self.greetings[idx]
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Скопировано", "Приветствие скопировано в буфер.")
    # --- Reactions tab ---
    def init_reactions_tab(self):
        frame = self.reactions_frame

        box = ttk.LabelFrame(frame, text="Банк STOP-реакций")
        box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.reactions_list = tk.Listbox(box, height=15)
        self.reactions_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.reactions_list.bind("<<ListboxSelect>>", self.on_reaction_select)

        react_edit = ttk.Frame(box)
        react_edit.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(react_edit, text="Текст реакции:").pack(side=tk.LEFT)
        self.reaction_var = tk.StringVar()
        ttk.Entry(react_edit, textvariable=self.reaction_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5
        )

        react_btns = ttk.Frame(box)
        react_btns.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(react_btns, text="Добавить", command=self.add_reaction).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(react_btns, text="Обновить", command=self.update_reaction).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(react_btns, text="Удалить", command=self.delete_reaction).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(
            react_btns,
            text="Копировать",
            command=self.copy_reaction_to_clipboard,
        ).pack(side=tk.LEFT, padx=2)

        self.refresh_reactions_list()
    def refresh_reactions_list(self):
        self.reactions_list.delete(0, tk.END)
        for r in self.reactions:
            self.reactions_list.insert(tk.END, r)

    def get_selected_reaction_index(self):
        selection = self.reactions_list.curselection()
        if not selection:
            return None
        return selection[0]

    def on_reaction_select(self, _event=None):
        idx = self.get_selected_reaction_index()
        if idx is None:
            return
        self.reaction_var.set(self.reactions[idx])

    def add_reaction(self):
        text = self.reaction_var.get().strip()
        if not text:
            return
        self.reactions.append(text)
        save_reactions(self.reactions)
        self.refresh_reactions_list()
        self.reaction_var.set("")

    def update_reaction(self):
        idx = self.get_selected_reaction_index()
        if idx is None:
            return
        text = self.reaction_var.get().strip()
        if not text:
            return
        self.reactions[idx] = text
        save_reactions(self.reactions)
        self.refresh_reactions_list()

    def delete_reaction(self):
        idx = self.get_selected_reaction_index()
        if idx is None:
            return
        if not messagebox.askyesno(
            "STOP-реакции", "Удалить выбранную реакцию из банка?"
        ):
            return
        self.reactions.pop(idx)
        if not self.reactions:
            self.reactions = list(REACTION_BLOCKS)
        save_reactions(self.reactions)
        self.refresh_reactions_list()

    def copy_reaction_to_clipboard(self):
        idx = self.get_selected_reaction_index()
        if idx is None:
            messagebox.showinfo("STOP-реакции", "Выберите реакцию для копирования.")
            return
        text = self.reactions[idx]
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Скопировано", "Текст реакции скопирован в буфер.")

    # --- Script tab ---
    def init_script_tab(self):
        top = ttk.Frame(self.script_frame)
        top.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(top, text="Время старта (например, 16:00):").grid(
            row=0, column=0, sticky="w"
        )
        self.start_time_var = tk.StringVar(value="16:00")
        ttk.Entry(top, textvariable=self.start_time_var, width=10).grid(
            row=0, column=1, sticky="w", padx=5
        )

        ttk.Button(
            top, text="Сгенерировать программу игры", command=self.generate_script
        ).grid(row=0, column=2, padx=10)

        ttk.Button(
            top, text="Скопировать текст в буфер", command=self.copy_script_to_clipboard
        ).grid(row=1, column=2, padx=10)

        ttk.Button(
            top, text="Очистить программу", command=self.clear_program_text
        ).grid(row=2, column=2, padx=10)

        # Выбор 10 ситуаций
        select_frame = ttk.LabelFrame(
            self.script_frame, text="Выбор ситуаций (до 10 штук)"
        )
        select_frame.pack(fill=tk.X, padx=5, pady=5)

        # подготовим варианты
        self.situation_choice_to_index = {}
        choices = []
        for idx, s in enumerate(self.situations):
            label = f"{idx+1}. {s.get('text','')[:70]}..."
            choices.append(label)
            self.situation_choice_to_index[label] = idx

        for i in range(10):
            row = ttk.Frame(select_frame)
            row.pack(fill=tk.X, pady=1)
            ttk.Label(row, text=f"Ситуация {i+1}:").pack(side=tk.LEFT)
            var = tk.StringVar()
            combo = ttk.Combobox(
                row,
                textvariable=var,
                values=choices,
                width=80,
                state="readonly",
            )
            combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.situation_select_vars.append(var)

        ttk.Button(
            select_frame,
            text="Заполнить случайно",
            command=self.fill_random_situations,
        ).pack(anchor="e", padx=5, pady=2)

        # Font controls
        font_frame = ttk.Frame(self.script_frame)
        font_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(font_frame, text="Шрифт:").pack(side=tk.LEFT)
        self.script_font_family_var = tk.StringVar(value="Segoe UI")
        self.script_font_size_var = tk.IntVar(value=12)
        font_family_combo = ttk.Combobox(
            font_frame,
            textvariable=self.script_font_family_var,
            values=["Segoe UI", "Arial", "Consolas"],
            width=15,
            state="readonly",
        )
        font_family_combo.pack(side=tk.LEFT, padx=5)
        size_spin = ttk.Spinbox(
            font_frame, from_=8, to=28, textvariable=self.script_font_size_var, width=4
        )
        size_spin.pack(side=tk.LEFT)
        ttk.Button(
            font_frame, text="Применить", command=self.update_script_font
        ).pack(side=tk.LEFT, padx=5)

        for i in range(3):
            top.rowconfigure(i, pad=2)

        self.script_text = tk.Text(self.script_frame, wrap=tk.WORD)
        self.script_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_script_font()

    def generate_script(self):
        start_time = self.start_time_var.get().strip() or "16:00"
        # Собираем выбранные ситуации из селектов
        indices: list[int] = []
        if self.situation_choice_to_index:
            for var in self.situation_select_vars:
                label = var.get()
                if not label:
                    continue
                idx = self.situation_choice_to_index.get(label)
                if idx is not None:
                    indices.append(idx)
        # если ничего не выбрано — рандомом
        if not indices:
            all_indices = list(range(len(self.situations)))
            random.shuffle(all_indices)
            indices = all_indices[: min(10, len(all_indices))]

        situations = [self.situations[i] for i in indices]
        count = len(situations)

        lines: list[str] = []
        # Приветствие берём из банка
        if self.greetings:
            template = random.choice(self.greetings)
        else:
            template = default_greetings()[0]
        try:
            greeting_text = template.format(start_time=start_time)
        except Exception:
            greeting_text = template
        lines.extend(greeting_text.splitlines())
        lines.append("")

        for idx, s in enumerate(situations, start=1):
            blocks_source = self.reactions if self.reactions else REACTION_BLOCKS
            block = random.choice(blocks_source)
            lines.append(block)
            lines.append("")
            prefix = "БОНУСНАЯ " if idx == count else ""
            lines.append(f"{prefix}СИТУАЦИЯ {idx}: {s.get('text')}")
            lines.append("")

        lines.append("⚡⚡⚡Уползаю считать КРУТЫЕ ЧЕРЕПА, не скучайте! ⚡⚡⚡")
        lines.append("")
        lines.append("Вы все КРУТЫЕ СКЕЛЕТЫ, НО РЕАЛЬНО КРУТЫМ ОКАЗАЛСЯ — __________")
        lines.append("")
        lines.append("🔥🔥🔥 ПОЗДРАВЛЯЕМ, ЭТО БЫЛА КРУТАЯ БИТВА!!!! 🔥🔥🔥")

        self.script_text.delete("1.0", tk.END)
        self.script_text.insert("1.0", "\n".join(lines))

    def update_script_font(self):
        family = self.script_font_family_var.get() or "Segoe UI"
        size = self.script_font_size_var.get() or 12
        try:
            self.script_font = tkfont.Font(family=family, size=int(size))
            self.script_text.configure(font=self.script_font)
        except Exception:
            pass

    def fill_random_situations(self):
        if not self.situations or not self.situation_choice_to_index:
            return
        choices = list(self.situation_choice_to_index.keys())
        random.shuffle(choices)
        # заполняем до 10 комбобоксов случайными различными ситуациями
        for i, var in enumerate(self.situation_select_vars):
            if i < len(choices):
                var.set(choices[i])
            else:
                var.set("")

    def copy_script_to_clipboard(self):
        text = self.script_text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Скопировано", "Текст программы игры скопирован в буфер.")

    def clear_program_text(self):
        """Очищает поле сгенерированной программы игры."""
        self.script_text.delete("1.0", tk.END)

    # --- Timer tab ---
    def init_timer_tab(self):
        frame = self.timer_frame

        desc = ttk.Label(
            frame,
            text=(
                "Таймер раунда.\n"
                "После того как отправил пост с ситуацией — жми «Старт».\n"
                "По умолчанию 3 минуты, можно настроить."
            ),
            justify=tk.LEFT,
        )
        desc.pack(pady=10)

        controls = ttk.Frame(frame)
        controls.pack(pady=5)

        ttk.Label(controls, text="Длительность (секунд):").grid(
            row=0, column=0, sticky="e"
        )
        self.timer_seconds_var = tk.IntVar(value=180)
        ttk.Spinbox(
            controls, from_=10, to=3600, textvariable=self.timer_seconds_var, width=7
        ).grid(row=0, column=1, padx=5)

        self.timer_label_var = tk.StringVar(value="03:00")
        timer_label = ttk.Label(
            frame, textvariable=self.timer_label_var, font=("Segoe UI", 32, "bold")
        )
        timer_label.pack(pady=20)

        btns = ttk.Frame(frame)
        btns.pack()

        ttk.Button(btns, text="Старт", command=self.start_timer).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btns, text="Стоп", command=self.stop_timer).pack(
            side=tk.LEFT, padx=5
        )

    def _format_seconds(self, seconds: int) -> str:
        m, s = divmod(max(0, seconds), 60)
        return f"{m:02d}:{s:02d}"

    def start_timer(self):
        self.stop_timer()
        seconds = self.timer_seconds_var.get()
        if seconds <= 0:
            seconds = 180
            self.timer_seconds_var.set(seconds)

        def on_tick(remain: int):
            self.after(0, lambda: self.timer_label_var.set(self._format_seconds(remain)))

        def on_done():
            def finish():
                self.timer_label_var.set("00:00")
                if winsound is not None:
                    try:
                        # системный звук Windows
                        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                        # дополнительный двойной Beep
                        winsound.Beep(1000, 700)
                        winsound.Beep(1400, 700)
                    except Exception:
                        pass
                messagebox.showinfo("Время!", "Время раунда вышло — пора считать реакции!")

            self.after(0, finish)

        self.current_timer = TimerThread(seconds, on_tick, on_done)
        self.current_timer.start()

    def stop_timer(self):
        if self.current_timer is not None:
            self.current_timer.stop()
            self.current_timer = None


def main():
    app = MemeGameApp()
    app.mainloop()


if __name__ == "__main__":
    main()

