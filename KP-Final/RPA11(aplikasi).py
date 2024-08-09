import schedule
import time
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import threading

# Fungsi untuk mengambil data tabel
def get_table_data(driver, modul, tabel):
    table = driver.find_element(By.XPATH, "//table[@class='table table-bordered table-striped']")
    headers = [header.text.strip() for header in table.find_elements(By.XPATH, ".//tr[2]/th")]
    rows = table.find_elements(By.XPATH, ".//tr[position() > 2]")

    data = []
    for row in rows:
        cols = row.find_elements(By.XPATH, ".//td")
        data.append([col.text.strip() for col in cols])
    for row in data:
        row.insert(0, tabel)
    for i in range(len(data)):
        for j in range(len(data[i])):
            try:
                data[i][j] = int(data[i][j])
            except ValueError:
                pass

    headers.insert(0, 'Tabel')
    return pd.DataFrame(data, columns=headers)

# Fungsi untuk menjalankan RPA
def run_rpa():
    print("RPA execution started.")
    start_time = time.time()
    service = Service(executable_path=r"D:\Kuliah things\SEMESTER 6\Magang\Proj\RPA\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://see.labs.telkomuniversity.ac.id/praktikum")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user_nim")))
    user_element = driver.find_element(By.NAME, "user_nim")
    user_element.clear()
    user_element.send_keys("1103213080")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user_pass")))
    user_element = driver.find_element(By.NAME, "user_pass")
    user_element.clear()
    user_element.send_keys("1103213080165")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login_ass")))
    select_element = Select(driver.find_element(By.NAME, "login_ass"))
    select_element.select_by_visible_text("Asisten")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "submit")))
    login_button = driver.find_element(By.NAME, "submit")
    login_button.click()

    all_data = {}
    for modul in range(1, 5):
        modul_data = pd.DataFrame()
        for tabel in range(1, 5):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'lihat_inputnilai')]")))
            lihat_hasil_input_link = driver.find_element(By.XPATH, "//a[contains(@href, 'lihat_inputnilai')]")
            lihat_hasil_input_link.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "modul_id")))
            modul_select = Select(driver.find_element(By.NAME, "modul_id"))
            modul_select.select_by_visible_text(f"Modul {modul}")

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"(//input[@value='view' and @role='button'])[{tabel}]")))
            view_button = driver.find_element(By.XPATH, f"(//input[@value='view' and @role='button'])[{tabel}]")
            driver.execute_script("arguments[0].click();", view_button)

            df = get_table_data(driver, f"Modul {modul}", f"Tabel {tabel}")
            modul_data = pd.concat([modul_data, df], ignore_index=True)
        all_data[f"Modul {modul}"] = modul_data

    combined_data = pd.concat(all_data.values(), ignore_index=True)
    combined_data[['TP', 'TA', 'D1', 'D2', 'D3', 'D4', 'I1', 'I2']] = combined_data[['TP', 'TA', 'D1', 'D2', 'D3', 'D4', 'I1', 'I2']].apply(pd.to_numeric, errors='coerce')
    combined_data['Rata-Rata'] = combined_data[['TP', 'TA', 'D1', 'D2', 'D3', 'D4', 'I1', 'I2']].mean(axis=1)

    average_data = combined_data.groupby('Nama')['Rata-Rata'].mean().reset_index()
    average_data['Rata-Rata'] = average_data['Rata-Rata'].round(2)

    output_path = r"D:\Kuliah things\SEMESTER 6\Magang\Proj\RPA\tabel_praktikum.xlsx"
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for sheet_name, df in all_data.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('C:C', 45)
            worksheet.set_column('M:M', 15)
        average_data.to_excel(writer, index=False, sheet_name='Rata-rata')
        worksheet = writer.sheets['Rata-rata']
        worksheet.set_column('A:A', 45)
        worksheet.set_column('B:B', 15)

    driver.quit()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
 
# Fungsi untuk menjadwalkan RPA
def schedule_rpa(date_string, time_string):
    run_datetime_str = f"{date_string} {time_string}"
    run_datetime = datetime.strptime(run_datetime_str, "%Y-%m-%d %H:%M")
    now = datetime.now()

    if run_datetime < now:
        messagebox.showerror("Error", "The given date and time have already passed.")
        return False

    schedule.every().day.at(run_datetime.strftime("%H:%M")).do(run_rpa)
    messagebox.showinfo("Scheduled", f"RPA scheduled to run on {run_datetime.strftime('%Y-%m-%d %H:%M')}")
    
    def schedule_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=schedule_loop).start()
    return True

# Fungsi untuk memulai jadwal
def start_schedule():
    input_date = date_var.get()
    input_time = time_var.get()
    if input_date.lower() == 'quit' or input_time.lower() == 'quit':
        messagebox.showinfo("Exit", "Exiting the scheduler.")
        app.quit()
    elif schedule_rpa(input_date, input_time):
        pass

# Fungsi untuk langsung menjalankan RPA
def start_rpa_immediately():
    threading.Thread(target=run_rpa).start()

# Membuat GUI dengan Tkinter
app = Tk()
app.title("RPA Scheduler")
app.geometry("500x600")
app.configure(bg='#f0f0f0')

style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12), background='#f0f0f0')
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TEntry', font=('Helvetica', 12), padding=5)

title_label = ttk.Label(app, text="RPA Scheduler", font=('Helvetica', 18, 'bold'))
title_label.pack(pady=20)

date_label = ttk.Label(app, text="Enter the date for RPA execution (YYYY-MM-DD):")
date_label.pack(pady=5)
date_var = StringVar()
date_entry = ttk.Entry(app, textvariable=date_var)
date_entry.pack(pady=5)

time_label = ttk.Label(app, text="Enter the time for RPA execution (HH:MM):")
time_label.pack(pady=5)
time_var = StringVar()
time_entry = ttk.Entry(app, textvariable=time_var)
time_entry.pack(pady=5)

schedule_button = ttk.Button(app, text="Schedule RPA", command=lambda: threading.Thread(target=start_schedule).start())
schedule_button.pack(pady=20)

run_button = ttk.Button(app, text="Run RPA Now", command=start_rpa_immediately)
run_button.pack(pady=20)

quit_button = ttk.Button(app, text="Quit", command=app.quit)
quit_button.pack(pady=10)

app.mainloop()
