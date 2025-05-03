import re
import os

# Klasör yollarını belirle
script_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\scripts"
dialogues_folder = "C:\\Users\\kerem\\Desktop\\DOĞAL DİL\\dialogues"

# Eğer dialogues klasörü yoksa oluştur
if not os.path.exists(dialogues_folder):
    os.makedirs(dialogues_folder)

def extract_character_dialogues(text):
    lines = text.split('\n')
    dialogues = []
    current_character = None
    dialogue_buffer = []

    for line in lines:
        # Karakter adlarını büyük harfli satırlardan tespit et
        match = re.match(r'^\s*([A-Z][A-Z0-9\(\)\. ]{2,})\s*$', line)
        if match:
            # Önceki karakterin diyaloglarını ekleyelim
            if current_character and dialogue_buffer:
                dialogues.append((current_character, ' '.join(dialogue_buffer)))
                dialogue_buffer = []
            
            # Yeni karakteri kaydet
            current_character = match.group(1)
        elif current_character and (line.startswith(' ') or line.startswith('\t')):
            # Eğer bir karakter belirlenmişse ve satır girintiliyse diyaloğa ekle
            dialogue_buffer.append(line.strip())
    
    # Son diyaloğu da ekle
    if current_character and dialogue_buffer:
        dialogues.append((current_character, ' '.join(dialogue_buffer)))

    return dialogues

# Tüm metin dosyalarını işle
for filename in os.listdir(script_folder):
    if filename.endswith(".txt"):  # Sadece .txt dosyalarını işle
        input_file = os.path.join(script_folder, filename)
        output_file = os.path.join(dialogues_folder, f"{filename.replace('.txt', '_dialogues.txt')}")

        # Dosyayı oku
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                script = f.read()
        except FileNotFoundError:
            print(f"Hata: Dosya {input_file} bulunamadı. Atlanıyor...")
            continue

        # Diyalogları ayıkla
        dialogues = extract_character_dialogues(script)

        # Diyalogları yeni bir dosyaya yaz
        with open(output_file, "w", encoding="utf-8") as f:
            for character, dialogue in dialogues:
                f.write(f"{character}: {dialogue}\n")

        print(f"Diyaloglar başarıyla '{output_file}' dosyasına yazıldı!")
