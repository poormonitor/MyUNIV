from main import app
from misc.func import process_excel
import sys

if len(sys.argv) < 3:
    filename = input("请输入文件路径：")
    year = int(input("请输入年份："))
    delete = False
else:
    filename = sys.argv[1]
    year = int(sys.argv[2])
    delete = True

process_excel(filename, year, delete)
