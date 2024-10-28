

"""
## pip install evtxtocsv

## https://pypi.org/project/evtxtocsv/

EVTX to CSV Converter, Windows olay günlüklerini (EVTX) CSV formatına dönüştürmek için kullanılan bir Python sınıfıdır. 
Bu sınıf, bir JSON dosyası içindeki olay günlüklerini okur ve her birini CSV dosyalarına dönüştürmek için gerekli komutları oluşturur.

"""
from evtx2csv.evtx2csv import EVTXToCSVConverter

EVTXToCSVConverter("Data Preparation\evtx_path.json")

