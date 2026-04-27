import re
from html import unescape

def deep_analyze_ui():
    with open('UI/Product - New - MinnoSoft.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print("=== DEEP UI ANALYSIS ===")
    
    # 1. Tìm tất cả các thẻ input và thuộc tính quan trọng
    inputs = re.findall(r'<input([^>]*?)>', content, re.DOTALL)
    print(f"\nFound {len(inputs)} inputs:")
    for i, inp in enumerate(inputs):
        name = re.search(r'name="([^"]+)"', inp)
        placeholder = re.search(r'placeholder="([^"]+)"', inp)
        type_attr = re.search(r'type="([^"]+)"', inp)
        id_attr = re.search(r'id="([^"]+)"', inp)
        print(f"{i}: name='{name.group(1) if name else 'N/A'}' | placeholder='{placeholder.group(1) if placeholder else 'N/A'}' | type='{type_attr.group(1) if type_attr else 'text'}' | id='{id_attr.group(1) if id_attr else 'N/A'}'")

    # 2. Tìm các textarea
    textareas = re.findall(r'<textarea([^>]*?)>', content, re.DOTALL)
    print(f"\nFound {len(textareas)} textareas:")
    for i, ta in enumerate(textareas):
        name = re.search(r'name="([^"]+)"', ta)
        print(f"{i}: name='{name.group(1) if name else 'N/A'}'")

    # 3. Tìm các button và role
    buttons = re.findall(r'<button([^>]*?)>(.*?)</button>', content, re.DOTALL)
    print(f"\nFound {len(buttons)} buttons:")
    for i, (attr, text) in enumerate(buttons):
        role = re.search(r'role="([^"]+)"', attr)
        aria_label = re.search(r'aria-label="([^"]+)"', attr)
        clean_text = re.sub(r'<[^>]*>', '', text).strip()
        if role or clean_text or aria_label:
            print(f"{i}: text='{clean_text[:30]}' | role='{role.group(1) if role else 'N/A'}' | aria-label='{aria_label.group(1) if aria_label else 'N/A'}'")

    # 4. Tìm các label
    labels = re.findall(r'<label[^>]*>(.*?)</label>', content, re.DOTALL)
    print(f"\nFound {len(labels)} labels:")
    for i, l in enumerate(labels):
        print(f"{i}: '{re.sub(r'<[^>]*>', '', l).strip()}'")

if __name__ == "__main__":
    deep_analyze_ui()
