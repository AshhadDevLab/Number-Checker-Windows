import subprocess
import pyautogui
import os
import time
import csv
import number_gen
from datetime import datetime
import customtkinter
import uuid
import glob
import AppOpener
import pygetwindow

current_date: datetime = datetime.now()
_init: bool = False
execution: bool = False
number_generator: any = None
    
def whatsapp_actions(_init: bool = False, _text: str = "+000000000000") -> None:
    # pyautogui.displayMousePosition()
    if _init:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(f'{_text}')
    else:
        pyautogui.moveTo(250, 75)
        pyautogui.click(250, 75)
        pyautogui.moveTo(275, 215)
        pyautogui.click(275, 215)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(f'{_text}')

def telegram_actions(_init: bool = False, _text: str = "+000000000000") -> None:
    if _init:
        pyautogui.moveTo(500, 445)
        pyautogui.click(500, 445)
        pyautogui.write(f'{_text}')
        pyautogui.press("tab", 2)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(f'{_text}')
        pyautogui.moveTo(560, 445)
        pyautogui.click(560, 445)
    else:
        pyautogui.moveTo(30, 50)
        pyautogui.click(30, 50)
        pyautogui.moveTo(30, 265)
        pyautogui.click(30, 265)
        pyautogui.moveTo(280, 550)
        pyautogui.click(280, 550)
        pyautogui.write(f'{_text}')
        pyautogui.press("tab", 2)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(f'{_text}')
        pyautogui.moveTo(530, 445)
        pyautogui.click(530, 445)

def write_data(application: str, _text: str, _no_result: bool) -> None:
    with open(f'data/{application}/{datetime.now().strftime("%Y-%m-%d")}.csv', mode='a', newline='') as file:
        writer: csv.writer = csv.writer(file)
        writer.writerow([_text, " No results found" if _no_result else " Results found"])
        log_textbox.insert(customtkinter.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {_text, " No results found" if _no_result else " Results found"}\n")

def application_actions(_text: str = "+000000000000", _failsafe: bool = True, _pause_timer: float = 1.25, application: str = "WhatsApp") -> None:
    global _init, _result_found
    pyautogui.PAUSE = _pause_timer
    pyautogui.FAILSAFE = _failsafe
    if application == "WhatsApp":
        whatsapp_actions(_text=_text, _init=_init)
    else:
        telegram_actions(_text=_text, _init=_init)
    _init = True  
    unique_id: uuid.UUID = uuid.uuid4()
    screenshot: pyautogui.Image = pyautogui.screenshot(region=(0, 0, 1600, 1600))
    screenshot.save(f"assets/{application}/screenshots/{_text}_{unique_id}.png")
    _result: pyautogui.Box | None = pyautogui.locateOnScreen(f'assets/{application}/reference.png', confidence=0.9)
    _result_found = not _result
    if _result_found and application == "Telegram":
        _init = False
    write_data(application, _text, _no_result=_result)

def data(application: str) -> str | None:
    list_of_files: list[str] = glob.glob(f'data/{application}/*.csv')
    if not list_of_files:
        return None
    latest_file: str = max(list_of_files, key=os.path.getctime)
    with open(latest_file, mode='r') as file:
        reader: csv.reader = csv.reader(file)
        rows: list[list[str]] = list(reader)
        if rows:
            return rows[-1][0]
        else:
            return None

def macro(application: str) -> None:
    global execution, number_generator
    if execution:
        try:
            number: str = next(number_generator)
            application_actions(application=application, _text=number)
        except StopIteration:
            execution = False
    app.after(1000, lambda: macro(get_application_name()))
    
def run_application(application: str) -> None:
    global execution, number_generator
    AppOpener.open(f"{application}", output=False)
    window = pygetwindow.getWindowsWithTitle(f'{application}')
    if len(window) > 0:
        print(window)
        window[0].resizeTo(800, 600)
        window[0].moveTo(0, 0)
    else:
        for _ in range(5):
            try:
                time.sleep(1)
                window = pygetwindow.getWindowsWithTitle(f'{application}')
                if len(window) > 0:
                    window[0].resizeTo(800, 600)
                    window[0].moveTo(0, 0)
                    break
            except Exception as e:
                print(f"Error: {e}")
                continue
    number_generator = number_gen.generate_numbers(_cont_number=data(get_application_name()))
    execution = True

def stop_application(application: str) -> None:
    global execution, _init
    try:
        execution = False
        _init = False
        AppOpener.close(f"{application}", output=False)
    except subprocess.CalledProcessError:
        print(f"Failed to stop {application}")

app: customtkinter.CTk = customtkinter.CTk()
app.geometry('600x500+800+0')
app.title('Number Checker')

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

start_button: customtkinter.CTkButton = customtkinter.CTkButton(app, text='Start', width=140, height=28, command=lambda: run_application(get_application_name()))
start_button.grid(row=1, column=0, padx=10, pady=10, sticky='e')

stop_button: customtkinter.CTkButton = customtkinter.CTkButton(app, text='Stop', width=140, height=28, command=lambda: stop_application(get_application_name()))
stop_button.grid(row=1, column=1, padx=10, pady=10, sticky='w')

options: list[str] = ["WhatsApp", "Telegram"]
selected_option: customtkinter.StringVar = customtkinter.StringVar(value=options[0])

dropdown: customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(app, variable=selected_option, values=options)
dropdown.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

def get_application_name() -> str:
    return selected_option.get()

log_textbox: customtkinter.CTkTextbox = customtkinter.CTkTextbox(app, width=580, height=300)
log_textbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

def log_message(message: str) -> None:
    log_textbox.insert(customtkinter.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    log_textbox.see(customtkinter.END)
    
log_message("Application started")

macro(get_application_name())

app.mainloop()