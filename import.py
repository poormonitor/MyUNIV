from server import app
from func import process_excel

filename = input("请输入文件路径：")
year = int(input("请输入年份："))

with app.app_context():
    process_excel(filename, year, True)
