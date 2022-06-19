from server import app
from func import process_excel

file = input("请输入文件路径：")
year = int(input("请输入年份："))

with app.app_context():
    process_excel(file, year, True)
