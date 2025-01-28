from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# Google Sheets API kaliti va ID
SERVICE_ACCOUNT_FILE = 'modified-hearth-445107-a7-51ed5f6f4110.json'
SPREADSHEET_ID = '1Xd0sNhai8Cdq4DkTgbDIBGy31wv6gcP3X10CMEDGd14'
RANGE_NAME = 'Sheet1!A:C'

# Google Sheets bilan bog'lanish va ma'lumotlarni olish
def get_google_sheets_data():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Ma'lumotlarni olish
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values

# Hozirgi va keyingi ko'rsatuvni hisoblash
def get_current_and_next_show(shows_data):
    # Toshkent vaqti
    tz = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tz)
    
    # Ko'rsatuvlar ma'lumotlarini olish
    current_show = None
    next_show = None
    
    for show in shows_data:
        show_name = show[0]
        start_time_str = show[1]
        end_time_str = show[2]
        
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').replace(year=now.year, month=now.month, day=now.day, tzinfo=tz)
            end_time = datetime.strptime(end_time_str, '%H:%M').replace(year=now.year, month=now.month, day=now.day, tzinfo=tz)
        except ValueError:
            continue

        # Hozirgi ko'rsatuvni topish
        if start_time <= now < end_time:
            current_show = {
                'name': show_name,
                'time_left': str(end_time - now).split('.')[0]  # tugashiga qancha vaqt qolgan
            }
        
        # Keyingi ko'rsatuvni topish
        if now < start_time:
            next_show = {
                'name': show_name,
                'start_time': start_time.strftime('%H:%M')  # boshlanish vaqti
            }
            break

    return current_show, next_show

@app.route('/')
def index():
    shows_data = get_google_sheets_data()
    current_show, next_show = get_current_and_next_show(shows_data)
    return render_template('index.html', current_show=current_show, next_show=next_show)

@app.route('/full_schedule')
def full_schedule():
    shows_data = get_google_sheets_data()
    return render_template('full_schedule.html', shows_data=shows_data)

if __name__ == '__main__':
    app.run(debug=True)
