import wfdb
import os
import matplotlib.pyplot as plt
import re  # Düzenli ifadeler için

# Grafiklerin kaydedileceği dizin
output_dir = "C:\\Users\\Escem\\OneDrive\\Desktop\\ekg"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# MIT-BIH Arrhythmia Database kayıt numaraları
record_numbers = [str(i).zfill(3) for i in range(100, 234)]

def clean_annotation_label(label):
    # Anotasyon etiketlerini temizleme
    return re.sub(r'\W+', '_', label)  # Tüm özel karakterleri '_' ile değiştir

for record_number in record_numbers:
    try:
        # Kaydı ve anotasyonları yükle
        record = wfdb.rdsamp(record_number, pn_dir='mitdb')
        annotation = wfdb.rdann(record_number, 'atr', pn_dir='mitdb')

        # Sinyali ayırma
        num_channels = record[0].shape[1]  # Kanal sayısını al
        print(f"{record_number} numaralı kayıt {num_channels} kanala sahip.")

        # İkinci kanalın var olup olmadığını kontrol et
        if num_channels > 1:
            sample_channel_1 = record[0][:, 0]  # İlk kanal
            sample_channel_2 = record[0][:, 1]  # İkinci kanal
        else:
            print(f"{record_number} numaralı kayıtta yeterli kanal bulunamadı.")
            continue  # Yeterli kanal yoksa bir sonraki kayda geç

        # Anotasyon etiketlerini alma
        annotation_labels = annotation.symbol

        # İlk 2000 örneği görselleştirme
        plt.figure(figsize=(15, 10))

        # İlk kanalın sinyali ve anotasyonları
        plt.subplot(2, 1, 1)
        plt.plot(sample_channel_1[:2000], label='Kanal 1', color='b')
        plt.scatter(annotation.sample[annotation.sample < 2000], 
                    sample_channel_1[annotation.sample[annotation.sample < 2000]], 
                    color='r', marker='x', label='Anotasyon')
        plt.title(f'{record_number} - Kanal 1 Sinyali ve Anotasyonlar')
        plt.xlabel("Örnek Sayısı")
        plt.ylabel("Genlik (mV)")
        plt.legend(loc='upper right')

        # İkinci kanalın sinyali ve anotasyonları
        plt.subplot(2, 1, 2)
        plt.plot(sample_channel_2[:2000], label='Kanal 2', color='g', alpha=0.7)
        plt.scatter(annotation.sample[annotation.sample < 2000], 
                    sample_channel_2[annotation.sample[annotation.sample < 2000]], 
                    color='r', marker='x', label='Anotasyon')
        plt.title(f'{record_number} - Kanal 2 Sinyali ve Anotasyonlar')
        plt.xlabel("Örnek Sayısı")
        plt.ylabel("Genlik (mV)")
        plt.legend(loc='upper right')

        plt.tight_layout()

        # Anotasyon etiketlerini dosya adı için uygun hale getirme
        cleaned_labels = [clean_annotation_label(label) for label in annotation_labels]
        unique_annotations = set(cleaned_labels)  # Anotasyon etiketlerinin benzersiz hali
        annotation_str = "_".join(sorted(unique_annotations))  # Benzersiz anotasyonları sıralı ve birleştirerek

        # Dosya ismi düzenlemesi
        file_name = f"{record_number}_{annotation_str}.png"

        # Grafik kaydetme
        plt.savefig(os.path.join(output_dir, file_name), dpi=300)
        plt.close()  # Grafiği kapatma

        # Anotasyon verilerini yazdırma
        print(f"{record_number} Numaralı Kayıt Anotasyonları: {annotation.__dict__}")

    except Exception as e:
        print(f"{record_number} numaralı kayıtta bir hata oluştu: {e}")
