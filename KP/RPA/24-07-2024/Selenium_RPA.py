from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

#Function Data Tabel
def get_table_data(driver, modul, tabel):
    table = driver.find_element(By.XPATH, "//table[@class='table table-bordered table-striped']")

    headers = [header.text.strip() for header in table.find_elements(By.XPATH, ".//tr[2]/th")]
    #baris
    rows = table.find_elements(By.XPATH, ".//tr[position() > 2]")

    data = []
    for row in rows:
        cols = row.find_elements(By.XPATH, ".//td")
        data.append([col.text.strip() for col in cols])

    #kolom
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

#Locate driver penghubung chrome
service = Service(executable_path=r"D:\Kuliah things\SEMESTER 6\Magang\Proj\RPA\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://see.labs.telkomuniversity.ac.id/praktikum")

# time.sleep(1)

# Username
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "user_nim"))
)
user_element = driver.find_element(By.NAME, "user_nim")
user_element.clear()
user_element.send_keys("1103213080")

# Password
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "user_pass"))
)
user_element = driver.find_element(By.NAME, "user_pass")
user_element.clear()
user_element.send_keys("1103213080165")

# Select Asisten
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "login_ass"))
)
select_element = Select(driver.find_element(By.NAME, "login_ass"))
select_element.select_by_visible_text("Asisten")

# Log Button
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "submit"))
)
login_button = driver.find_element(By.NAME, "submit")
login_button.click()

# Variabel untuk menyimpan semua DataFrame
all_data = {}

# Loop Modul dan Tabel
for modul in range(1, 5):
    modul_data = pd.DataFrame()
    for tabel in range(1, 5):
        # Lihat hasil input
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'lihat_inputnilai')]"))
        )
        lihat_hasil_input_link = driver.find_element(By.XPATH, "//a[contains(@href, 'lihat_inputnilai')]")
        lihat_hasil_input_link.click()

        # Pilih Modul
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "modul_id"))
        )
        modul_select = Select(driver.find_element(By.NAME, "modul_id"))
        modul_select.select_by_visible_text(f"Modul {modul}")

        # View Tabel
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"(//input[@value='view' and @role='button'])[{tabel}]"))
        )
        view_button = driver.find_element(By.XPATH, f"(//input[@value='view' and @role='button'])[{tabel}]")
        driver.execute_script("arguments[0].click();", view_button)

        # time.sleep(0.5)

        df = get_table_data(driver, f"Modul {modul}", f"Tabel {tabel}")
        modul_data = pd.concat([modul_data, df], ignore_index=True)

    # Simpan data modul ke dalam dictionary
    all_data[f"Modul {modul}"] = modul_data

combined_data = pd.concat(all_data.values(), ignore_index=True)

combined_data[['TP', 'TA', 'D1', 'D2', 'D3', 'D4', 'I1', 'I2']] = combined_data[['TP', 'TA', 'D1', 'D2', 'D3', 'D4', 'I1', 'I2']].apply(pd.to_numeric, errors='coerce')
combined_data['Rata-Rata'] = combined_data[['TP', 'TA', 'D1', 'D2', 'D3', 'D4', 'I1', 'I2']].mean(axis=1)

average_data = combined_data.groupby('Nama')['Rata-Rata'].mean().reset_index()
average_data['Rata-Rata'] = average_data['Rata-Rata'].round(2) 

#menyimpan dataframe ke excel
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
