import re
import os

def analyze_comboboxes():
    file_path = 'UI/Product - New - MinnoSoft.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tìm tất cả button role="combobox"
    comboboxes = re.finditer(r'<button[^>]*role="combobox"[^>]*>', content)
    
    print("--- COMBOBOXES AND THEIR CONTEXT ---")
    for i, cb_match in enumerate(comboboxes):
        # Tìm label gần nhất phía trước (trong khoảng 500 ký tự)
        start_search = max(0, cb_match.start() - 500)
        context_before = content[start_search:cb_match.start()]
        
        labels = re.findall(r'<label[^>]*>(.*?)</label>', context_before, re.DOTALL)
        last_label = re.sub(r'<[^>]*>', '', labels[-1]).strip() if labels else "N/A"
        
        print(f"COMBOBOX {i+1}: index={cb_match.start()}, label='{last_label}'")
        # Print actual button tag
        print(f"  TAG: {cb_match.group(0)}")

if __name__ == "__main__":
    analyze_comboboxes()
