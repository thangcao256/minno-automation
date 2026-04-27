import os

path = '../test_data/product_data.py'
image_default = [r"D:\CODE\minno-automation\test_data\logo.png"]

content = f"""# Dữ liệu mẫu cho Module Sản phẩm
PRODUCT_TEST_DATA = {{
    # 1. Sản phẩm đơn giản, không quản lý kho
    "basic_product": {{
        "name": "Sản phẩm Đơn Test 001",
        "SKU": "SKU-BASIC-001",
        "barcode": "893001001",
        "note": "Hàng tặng kèm, không quản lý kho",
        "group": "Nhóm 2504_0851",
        "category": "Danh mục 2504_0841",
        "supplier": "Nguồn hàng 2504_1007",
        "status": "Active",
        "for_sale": True,
        "has_variants": False,
        "wholesale_price": 50000,
        "sale_price": 75000,
        "manage_inventory": False,
        "images": {image_default}
    }},

    # 2. Sản phẩm quản lý kho, không bán âm
    "inventory_product": {{
        "name": "Sản phẩm Kho Test 002",
        "SKU": "SKU-INV-002",
        "barcode": "893001002",
        "group": "Nhóm 2504_0851",
        "category": "Danh mục 2504_0841",
        "status": "Active",
        "for_sale": True,
        "has_variants": False,
        "wholesale_price": 120000,
        "sale_price": 200000,
        "manage_inventory": True,
        "allow_negative": False,
        "total_stock": 50,
        "images": {image_default}
    }},

    # 3. Sản phẩm có Lô & Hạn sử dụng, cho phép bán âm
    "batch_expiry_product": {{
        "name": "Sản phẩm Lô/Hạn dùng 003",
        "SKU": "SKU-BATCH-003",
        "barcode": "893001003",
        "group": "Nhóm 2504_0851",
        "category": "Danh mục 2504_0841",
        "status": "Active",
        "for_sale": True,
        "has_variants": False,
        "wholesale_price": 300000,
        "sale_price": 450000,
        "manage_inventory": True,
        "allow_negative": True,
        "batch_name": "LOT-JUNE-2026",
        "expiry_date": "31/12/2026",
        "total_stock": 100,
        "images": {image_default}
    }},

    # 4. Sản phẩm có nhiều biến thể (Variants)
    "variants_product": {{
        "name": "Áo Thun Nam Cao Cấp 004",
        "SKU": "SKU-VAR-004",
        "group": "Nhóm Hàng Hiệu 2304_1350",
        "category": "Danh mục 2504_0841",
        "status": "Active",
        "for_sale": True,
        "has_variants": True,
        "variants_config": [
            {{
                "attribute": "Color",
                "values": ["Red", "Blue"]
            }},
            {{
                "attribute": "Size",
                "values": ["M", "L"]
            }}
        ],
        "manage_inventory": True,
        "allow_negative": False,
        "images": {image_default}
    }}
}}
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Successfully updated {{path}} with images")
