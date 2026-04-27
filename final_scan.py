import re

def analyze_all_fields():
    with open('UI/Product - New - MinnoSoft.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print("=== FULL FIELD SCAN ===")
    
    # Tìm tất cả các đoạn văn bản có vẻ là nhãn trường (Label)
    # Thường nằm trong <label> hoặc <p> hoặc <span> cạnh input
    labels = re.findall(r'<label[^>]*>(.*?)</label>', content, re.DOTALL)
    for l in labels:
        clean = re.sub(r'<[^>]*>', '', l).strip()
        if clean:
            print(f"LABEL: {clean}")

    # Tìm các Radio groups (Quản lý kho, Dùng để bán...)
    print("\n--- RADIO OPTIONS ---")
    radios = re.findall(r'role="radio"[^>]*value="([^"]+)"[^>]*aria-checked="([^"]+)"', content)
    for val, checked in radios:
        print(f"RADIO: value={val}, checked={checked}")

    # Tìm các Input không có name nhưng có label đi kèm
    print("\n--- INPUTS WITHOUT NAME ---")
    matches = re.finditer(r'<label[^>]*>(.*?)</label>.*?<input([^>]*?)>', content, re.DOTALL)
    for m in matches:
        lbl = re.sub(r'<[^>]*>', '', m.group(1)).strip()
        attrs = m.group(2)
        if 'name=' not in attrs:
            print(f"INPUT for '{lbl}': {attrs[:100]}...")

    # Tìm section Tồn kho cụ thể
    if 'Tồn kho' in content:
        print("\n--- STOCK SECTION FOUND ---")
        idx = content.find('Tồn kho')
        print(content[idx:idx+1000])

analyze_all_fields()
