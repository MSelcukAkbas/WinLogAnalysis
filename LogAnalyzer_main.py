import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from duckduckgo_search import DDGS

class LogAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['TimeCreated'] = pd.to_datetime(self.df['TimeCreated'], dayfirst=True)
        self.filtered_df = self.df.copy()

        self.event_log_descriptions = {
            4624: "Kullanıcının başarılı oturum açması.",
            4625: "Başarısız oturum açma durumu.",
            1102: "Logların silindikten sonra oluşan logları.",
            4634: "Kullanıcının oturum kapatması ile ilgili olaylar.",
            4776: "Yetkilendirme başarısızlığı, yanlış şifre gibi.",
            7045: "Hizmet başlangıcı veya durdurulması.",
            10016: "Uygulamanın COM bileşenine erişim izni yok.",
            41: "Sistem beklenmedik şekilde yeniden başlatıldı veya kapandı.",
            4663: "Nesne izinlerine erişim girişimlerini izler."
        }

    def check_empty(self):
        return self.filtered_df.empty

    def analyze_log_level(self):
        log_seviyesi = self.filtered_df['LevelDisplayName'].value_counts()
        return log_seviyesi

    def analyze_trend(self):
        trend = self.df['TimeCreated'].dt.date.value_counts().sort_index()
        return trend

    def filter_data(self, column, value):
        self.filtered_df = self.df[self.df[column] == value]

    def filter_by_importance(self, importance_level):
        self.filtered_df = self.df[self.df['LevelDisplayName'] == importance_level]

    def summary_statistics(self):
        return self.df.describe()

    def analyze_time_range(self, start_date, end_date):
        mask = (self.df['TimeCreated'] >= start_date) & (self.df['TimeCreated'] <= end_date)
        return self.df.loc[mask]

    def calculate_error_rate(self):
        trend = self.analyze_trend()
        return trend.mean()

    def ilk_log_tarihi(self):
        return self.df['TimeCreated'].min()

    def son_log_tarihi(self):
        return self.df['TimeCreated'].max()

    def save_to_json(self, file_name='filtered_log_data.json'):
        self.filtered_df.to_json(file_name, orient='records', lines=True)

    def search_solutions(self, trend):
        mesaj = f"""
            Sen bir sistem yöneticisi olarak düşün. Aşağıdaki veriyi yorumla ve hatalı uygulamalar hakkında önerilerde bulun. 
            Veri: {str(self.filtered_df[["TimeCreated", 'Message', 'Level', "LevelDisplayName", "LogName", "ProviderName"]].head(1000))}
            hataların zaman bazlı eğilimi Zaman Bazlı Hata Eğilimleri:
            {str(trend)}
            Lütfen aşağıdaki konulara odaklan:
            1. Aşağıda belirtilen hatalı uygulamaları ve hata mesajlarını analiz et.
            2. Her bir hata için belirli çözüm önerilerini sun.
            3. Kullanıcıların bu hatalarla başa çıkmalarına yardımcı olacak adım adım yönergeler oluştur.
            4. Uygulama hatalarının sistem üzerindeki etkilerini değerlendir.
        """
        ddgs = DDGS()
        results = ddgs.chat(mesaj)
        return results

    def map_event_descriptions(self):
        self.filtered_df['EventDescription'] = self.filtered_df['Level'].map(self.event_log_descriptions)

    def plot_trend(self, trend):
        plt.figure(figsize=(12, 6))
        plt.plot(trend.index, trend.values, marker='o', label='Hata Sayısı')
        plt.title('Zaman Bazlı Hata Eğilimleri')
        plt.xlabel('Tarih')
        plt.ylabel('Hata Sayısı')
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.show()

    def run_analysis(self):
        if not self.check_empty():
            print(f"Toplam veri sayısı: {len(self.df)}")
            self.filter_by_importance('Error') 
            print(f"Filtrelenmiş veri sayısı: {len(self.filtered_df)}")
            self.map_event_descriptions() 
            log_seviyesi = self.analyze_log_level()
            trend = self.analyze_trend()
            self.search_solutions(trend)
            self.plot_trend(trend)

# Kullanım örneği
if __name__ == "__main__":
    analyzer = LogAnalyzer('data\\Security2.csv')
    
    print("İlk Log Tarihi:", analyzer.ilk_log_tarihi())
    print("Son Log Tarihi:", analyzer.son_log_tarihi())
    
    print("Filtrelenmiş Verinin Özeti:\n", analyzer.summary_statistics())
    
    error_rate = analyzer.calculate_error_rate()
    print("Ortalama Hata Sayısı:\n", error_rate)

    analyzer.run_analysis()
    
    print("Filtrelenmiş Verideki Olay Açıklamaları:\n", analyzer.filtered_df[['Level', 'EventDescription']].head(10))
