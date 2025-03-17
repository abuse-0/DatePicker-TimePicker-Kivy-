# DatePicker/TimePicker (Kivy)
from kivy.uix.actionbar import BoxLayout
from kivy.uix.filechooser import ScreenManager
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.uix.label import Label

import json

import kivy
kivy.require("2.3.0")

from kivy.core.window import Window
Window.clearcolor = (1, 0.75, 0.8, 1)  # Розовый фон

kv = """
# height: self.minimum_height - без этого ScrollView всегда вверх уходит
# size_hint_y: None - отключает автоматическую настрйку высоты
#:import Factory kivy.factory.Factory

<ErrorPopup@Popup>:
    title: "Что то не выбрано"

    auto_dismiss: False
    size_hint: 0.4, 0.4
    Button:
        text: 'ого'
        on_release: root.dismiss()

<SuccessPopup@Popup>:
    title: "Сохранено"

    auto_dismiss: False
    size_hint: 0.4, 0.4
    Button:
        text: 'ага'
        on_release: root.dismiss()

<DatePopup@Popup>:
    size_hint: (0.8, 0.6)
    title: "Выберите дату"

    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10

        GridLayout:
            cols: 3
            spacing: 10
            padding: 10

            Spinner:
                id: year_spinner
                text: "Год"
                values: ["2025"]
                size_hint_y: None
                height: "40dp"

            Spinner:
                id: month_spinner
                text: "Месяц"
                values: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
                size_hint_y: None
                height: "40dp"
                on_text: app.update_days(root) # Это что ваще............

            Spinner:
                id: day_spinner
                text: "Сначала выбери месяц"
                font_size: "16sp" # ага(числа пипец маленькие кнш тут)
                size_hint_y: None
                height: "40dp"

        GridLayout:
            cols: 2
            spacing: 10
            padding: 10

            Button:
                text: "Сохранить"
                on_release: 
                    app.save_date(root)

            Button:
                text: "Назад"
                on_release: root.dismiss()

<FilterDatePopup@Popup>:
    size_hint: (0.8, 0.6)
    title: "Выберите дату"

    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10

        GridLayout:
            cols: 3
            spacing: 10
            padding: 10

            Spinner:
                id: filter_year_spinner
                text: "Год"
                values: ["2025"]
                size_hint_y: None
                height: "40dp"

            Spinner:
                id: filter_month_spinner
                text: "Месяц"
                values: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
                size_hint_y: None
                height: "40dp"
                on_text: app.filter_update_days(root) # Это что ваще............

            Spinner:
                id: filter_day_spinner
                text: "Сначала выбери месяц"
                font_size: "16sp" # ага(числа пипец маленькие кнш тут)
                size_hint_y: None
                height: "40dp"

        GridLayout:
            cols: 2
            spacing: 10
            padding: 10

            Button:
                text: "Сохранить"
                on_release: 
                    app.save_filter_date(root)

            Button:
                text: "Назад"
                on_release: root.dismiss()        
                

<TimePopup@Popup>:
    size_hint: (0.8, 0.6)
    title: "Выберите Время"

    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10

        GridLayout:
            cols: 3
            spacing: 10
            padding: 10

# Как же это долго листать

            Spinner:
                id: hour_spinner
                text: "Часы"
                values: [str(i) for i in range(1, 25)]
                size_hint_y: None
                height: "40dp"

            Spinner:
                id: minute_spinner
                text: "Минуты"
                values: [str(i) for i in range(1, 61)]
                size_hint_y: None
                height: "40dp"

            Spinner:
                id: second_spinner
                text: "Секунды"
                values: [str(i) for i in range(1, 61)]
                size_hint_y: None
                height: "40dp"

        GridLayout:
            cols: 2
            spacing: 10
            padding: 10

            Button:
                text: "Сохранить"
                on_release: 
                    app.save_time(root)

            Button:
                text: "Назад"
                on_release: root.dismiss()

WindowManager:
    MainScreen:
    ListOfEventsScreen:
    AddNewEventScreen:
    
<Label>:
    font_size: "24sp"
    color: 1, 0.5, 0.5, 1
    font_name: "Comic"

<MainScreen>:
    name: "main_screen"
    
    BoxLayout:
        orientation: "vertical"
        padding:10
        spacing:10

        Label:
            text: "йоу"
            color: 0, 0, 0, 1  # ага

        GridLayout:
            cols: 2
            spacing: 10
            padding: 10

            Button:
                text: "Добавить событие"

                on_release:
                    app.root.current = "add_new_event_screen"
                    root.manager.transition.direction = "right"


            Button:
                text: "Список событий"
                
                on_release:
                    app.root.current = "list_of_events_screen"
                    root.manager.transition.direction = "left"

<AddNewEventScreen>:
    name: "add_new_event_screen"

# Зачем я тут это чередовал если по итогу с грид было бы тоже самое о.О

    BoxLayout:
        orientation: "vertical"
        padding:10
        spacing:10

        GridLayout:
            cols: 2
            spacing: 10
            padding: 10
        
            Button: 
                id: select_date_button
                text: "Выбрать дату"

                on_release: app.show_date_popup()

            Button:
                id: select_time_button
                text: "Выбрать время"

                on_release: app.show_time_popup()

            Label:
                text: "Название:"
                color: 0, 0, 0, 1  # ага

            TextInput:
                id: events_name
        
        GridLayout:
            cols: 2
            spacing: 10
            padding: 10

            Label:
                text: "Описание:"
                color: 0, 0, 0, 1  # ага

            TextInput:
                id: add_event_description

            Button:
                text: "Сохранить"

                on_release:
                    app.save_event()

            Button:
                text: "Назад"

                on_release: 
                    app.root.current = "main_screen"
                    root.manager.transition.direction = "left"

<ListOfEventsScreen>:
    name: "list_of_events_screen"    

    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)

        Label:
            text: "Чтобы применить фильтр: выбери дату, затем нажми на кнопку фильтр"
            color: 0, 0, 0, 1  # ага
            font_size: "20sp"
            size_hint_y: None # Фиксированная высота для всех кнопок
            height: dp(30)

        GridLayout:
            cols: 3
            spacing: dp(5)
            padding: dp(10)

            size_hint_y: None  # Фиксированная высота для всех кнопок(не авто)
            height: dp(75)  # Высота всей строки кнопок

            Button:
                text: "Выбрать дату"
                size_hint_y: None
                height: dp(50)

                on_release: app.show_filter_date_popup()

            Button:
                text: "Фильтр"
                size_hint_y: None
                height: dp(50)

                on_release: 
                    app.event_date_filter()
                    app.load_event()

            Button:
                text: "Сбросить фильтр"
                size_hint_y: None
                height: dp(50)

                on_release: 
                    app.reset_date_filter()
                    app.load_event()

        ScrollView:
            GridLayout:
                id: event_list
                cols: 1
                spacing: dp(10)
                padding: dp(10)
                size_hint_y: None  

        Button:
            text: "Назад"
            size_hint_y: None
            height: dp(50)

            on_release:
                app.root.current = "main_screen"
                root.manager.transition.direction = "right"

"""

# При каждом запуске []
with open("events.json", "w") as f:
    f.write("[\n]")

DAYS_IN_MONTH = {
        "Январь": 31, "Февраль": 28, "Март": 31, "Апрель": 30, "Май": 31, "Июнь": 30,
        "Июль": 31, "Август": 31, "Сентябрь": 30, "Октябрь": 31, "Ноябрь": 30, "Декабрь": 31
    }

class MainScreen(Screen):
    pass

class ListOfEventsScreen(Screen):
    # При переходе на этот экран загружает виджеты 
    def on_pre_enter(self):
        app = App.get_running_app()
        app.load_event()

class AddNewEventScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyMainApp(App):
    def __init__(self, **kwargs):
        # Без этого оно не запускается со списками
        super().__init__(**kwargs)
        self.time_list = []
        self.date_list = []
        self.filter_date_list = []
        self.main_date_filter = []
    
    def build(self):
        return Builder.load_string(kv)
    
    def update_days(self, popup):
        # Получаем элементы внутри попапа
        month_spinner = popup.ids.month_spinner
        day_spinner = popup.ids.day_spinner

        selected_month = month_spinner.text
        if selected_month in DAYS_IN_MONTH:
            days_in_month = DAYS_IN_MONTH[selected_month]
            day_spinner.values = [str(day) for day in range(1, days_in_month + 1)]
            day_spinner.text = "1" # Чтобы всегда не висело "Сначала выбери месяц"

    def filter_update_days(self, popup):
        # Получаем элементы внутри попапа
        month_spinner = popup.ids.filter_month_spinner
        day_spinner = popup.ids.filter_day_spinner

        selected_month = month_spinner.text
        if selected_month in DAYS_IN_MONTH:
            days_in_month = DAYS_IN_MONTH[selected_month]
            day_spinner.values = [str(day) for day in range(1, days_in_month + 1)]
            day_spinner.text = "1" # Чтобы всегда не висело "Сначала выбери месяц"
    
    def show_date_popup(self):
        popup = Factory.DatePopup()
        popup.open()

    def show_filter_date_popup(self):
        popup = Factory.FilterDatePopup()
        popup.open()

    def show_time_popup(self):
        popup = Factory.TimePopup()
        popup.open()

    def show_error_popup(self):
        popup = Factory.ErrorPopup()
        popup.open()

    def show_success_popup(self):
        popup = Factory.SuccessPopup()
        popup.open()

    def save_date(self, popup):
        day = popup.ids.day_spinner.text
        month = popup.ids.month_spinner.text
        year = popup.ids.year_spinner.text

        if day != "Сначала выбери месяц" and month != "Месяц" and year != "Год":
            self.date_list = []
            
            self.date_list.append(day)
            self.date_list.append(month)
            self.date_list.append(year)
            popup.dismiss()
            print(self.date_list)
        else:
            self.show_error_popup()

    def save_filter_date(self, popup):
        day = popup.ids.filter_day_spinner.text
        month = popup.ids.filter_month_spinner.text
        year = popup.ids.filter_year_spinner.text

        if day != "Сначала выбери месяц" and month != "Месяц" and year != "Год":
            self.filter_date_list = []
            
            self.filter_date_list.append(day)
            self.filter_date_list.append(month)
            self.filter_date_list.append(year)
            popup.dismiss()
            print(self.filter_date_list)
        else:
            self.show_error_popup()

    def save_time(self, popup):
        second = popup.ids.second_spinner.text
        minute = popup.ids.minute_spinner.text
        hour = popup.ids.hour_spinner.text

        if hour != "Часы" and minute != "Минуты" and second != "Секунды":
            self.time_list = []

            self.time_list.append(hour)
            self.time_list.append(minute)
            self.time_list.append(second)
            popup.dismiss()
            print(self.time_list)
        else:
            self.show_error_popup()


    def save_event(self):
        # Сохранить все и очистить после сейва, при сохранении проверять, что все введено
        add_new_event_screen = self.root.get_screen("add_new_event_screen")
        event_name = add_new_event_screen.ids.events_name.text
        event_description = add_new_event_screen.ids.add_event_description.text

        if event_name and event_description and len(self.time_list) == 3 and len(self.date_list) == 3:
            print(event_name, event_description)
            print(self.time_list)
            print(self.date_list)
            date = ' '.join(self.date_list)
            time = ':'.join(self.time_list)

            # Название, дата, время, описание
            event_to_save = {"name": event_name, "date": date, "time": time, "description": event_description}

            with open("events.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            data.append(event_to_save)

            with open("events.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.show_success_popup()

            add_new_event_screen.ids.events_name.text = ""
            add_new_event_screen.ids.add_event_description.text = ""
            self.time_list = []
            self.date_list = []

        else:
            self.show_error_popup()

    def load_event(self):
        list_screen = self.root.get_screen("list_of_events_screen")
        events_list = list_screen.ids.event_list
        events_list.clear_widgets()

        try:
            with open("events.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []
        found_events = False  # Флаг для проверки наличия событий

        for event in data:
            if event['date'] == ' '.join(self.main_date_filter) or self.main_date_filter == []:
                event_box = BoxLayout(orientation="vertical", padding=10, spacing=5, size_hint_y=None)
                event_box.add_widget(Label(text=f"[b]{event['name']}[/b]", markup=True, font_size="20sp", color=(0, 0, 0, 1)))
                event_box.add_widget(Label(text=f"Дата: {event['date']}", font_size="16sp", color=(0, 0, 0, 1)))
                event_box.add_widget(Label(text=f"Время(часы:минуты:секунды): {event['time']}", font_size="16sp", color=(0, 0, 0, 1)))
                event_box.add_widget(Label(text=f"Описание: {event['description']}", font_size="16sp", color=(0, 0, 0, 1)))
                events_list.add_widget(event_box)
                found_events = True  # Найдено хотя бы одно событие

        if not found_events:
            events_list.add_widget(Label(text="Нет событий", font_size="25sp", color=(0, 0, 0, 1)))
            
    # Тут нужно получить как то 
    def event_date_filter(self):
        self.main_date_filter = self.filter_date_list
        print(self.main_date_filter)

    def reset_date_filter(self):
        self.main_date_filter = []
        print(self.main_date_filter)

if __name__ == "__main__":
    MyMainApp().run()
