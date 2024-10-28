import pandas as pd

# CSV dosyasını oku ve hata kontrolü yap
try:
    df = pd.read_csv('data/Application.csv', encoding='utf-8')
except FileNotFoundError:
    print("Dosya bulunamadı. Lütfen dosya yolunu kontrol edin.")
    exit()
except pd.errors.EmptyDataError:
    print("Dosya boş. Lütfen geçerli bir dosya yükleyin.")
    exit()
except Exception as e:
    print(f"Bilinmeyen bir hata oluştu: {e}")
    exit()

###########################################################

# Boş sütunları kaldır
df_cleaned = df.dropna(how='all', axis=1)

###########################################################

# Belirli hatalı formatlara göre veri temizleme
df_cleaned = df_cleaned.applymap(lambda x: x.strip() if isinstance(x, str) else x)

###########################################################

# Sütun isimlerini standartlaştır
df_cleaned.columns = df_cleaned.columns.str.strip().str.lower().str.replace(' ', '_')

# Temizlenmiş veri çerçevesini kontrol et
print(df_cleaned.head())

###########################################################

# CSV dosyasının ilk satırını siliyoruz
df = pd.read_csv('data/Application.csv', skiprows=1)

df.to_csv('data/Application2.csv', index=False)

###########################################################

# Temizlenmiş CSV'yi kaydet
df_cleaned.to_csv('data/Application2.csv', index=False, encoding='utf-8')
