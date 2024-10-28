import pandas as pd
import matplotlib.pyplot as plt
from duckduckgo_search import DDGS

class LogAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.df['TimeCreated'] = pd.to_datetime(self.df['TimeCreated'], dayfirst=True)
        if self.df.empty:
            print("Veri boş ya da hatalı")
        
        self.filtered_df = self.df.copy()

    def get_first_and_last_log_dates(self):
        return self.df['TimeCreated'].min(), self.df['TimeCreated'].max()

    def save_filtered_logs_to_json(self, file_name='filtered_log_data.json'):
        self.filtered_df.to_json(file_name, orient='records', lines=True)

    def get_log_level_distribution(self):
        return self.filtered_df['LevelDisplayName'].value_counts()

    def get_event_trend_by_date(self):
        return self.df['TimeCreated'].dt.date.value_counts().sort_index()

    def filter_logs_by_column_value(self, column, value):
        self.filtered_df = self.df[self.df[column] == value]
        return self.filtered_df

    def filter_logs_by_date_range(self, start_date, end_date):
        mask = (self.df['TimeCreated'] >= start_date) & (self.df['TimeCreated'] <= end_date)
        return self.df.loc[mask]

    def calculate_average_daily_log_count(self):
        trend = self.get_event_trend_by_date()
        return trend.mean().__round__()

    def search_for_error_solutions(self, trend , average_daily , distribution ):

        mesaj = f"""
        Sen bir sistem yöneticisi olarak düşün. Aşağıdaki veriyi yorumla ve hatalı uygulamalar hakkında önerilerde bulun. 

        Veri:
        {str(self.filtered_df[["TimeCreated", 'Message', 'Level', "LevelDisplayName", "LogName", "ProviderName"]].head(1000))}

        Hataların zaman bazlı eğilimi: 
        Zaman Bazlı Hata Eğilimleri:
        {str(trend)}

        ------------------------

        Ortalama günlük hata: 
        {str(average_daily)}

        ------------------------

        Log seviyeleri dağılımı: 
        {str(distribution)}

        ------------------------

        Lütfen aşağıdaki konulara odaklan:
        1. Aşağıda belirtilen hatalı uygulamaları ve hata mesajlarını analiz et.
        2. Her bir hata için belirli çözüm önerilerini sun.
        3. Kullanıcıların bu hatalarla başa çıkmalarına yardımcı olacak adım adım yönergeler oluştur.
        4. Uygulama hatalarının sistem üzerindeki etkilerini değerlendir.
        """
        ddgs = DDGS()
        results = ddgs.chat(mesaj)
        return results


    def plot_event_trend_graph(self, trend):
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

if __name__ == "__main__":
    analyzer = LogAnalyzer('data\\System2.csv')

    first_date, last_date = analyzer.get_first_and_last_log_dates()

    log_level_distribution = analyzer.get_log_level_distribution()

    event_trend = analyzer.get_event_trend_by_date()

    average_daily_logs = analyzer.calculate_average_daily_log_count()

    error_solutions = analyzer.search_for_error_solutions(event_trend , average_daily=average_daily_logs , distribution=log_level_distribution)
    print("Hata Çözüm Önerileri:\n", error_solutions)
