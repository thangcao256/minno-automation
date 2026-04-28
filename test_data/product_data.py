import time
import os

def get_run_id():
    return time.strftime("%d%m_%H%M")

run_id = get_run_id()

# Đường dẫn ảnh mặc định (Sử dụng đường dẫn tuyệt đối)
current_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IMAGE = os.path.join(current_dir, "logo.png")

# Ma trận bao phủ toàn bộ các trường hợp sản phẩm
PRODUCT_MATRIX_DATA = {
    # 1. Simple, For Sale, No Inventory
    "S1_V1_I1": {
        "name": f"SP Dịch Vụ {run_id}",
        "SKU": f"SKU-S1V1I1-{run_id}",
        "for_sale": True,
        "has_variants": False,
        "manage_inventory": False,
        "sale_price": 50000,
        "category": "Danh mục 2504_0841",
        "group": "Nhóm 2504_0851",
        "images": [DEFAULT_IMAGE]
    },
    # 2. Simple, For Sale, Inventory, No Negative
    "S1_V1_I2_N1": {
        "name": f"SP Kho Chuẩn {run_id}",
        "SKU": f"SKU-S1V1I2N1-{run_id}",
        "for_sale": True,
        "has_variants": False,
        "manage_inventory": True,
        "allow_negative": False,
        "batch_name": f"BATCH-STD-{run_id}",
        "expiry_date": "25/12/2026",
        "total_stock": 50,
        "sale_price": 100000,
        "category": "Danh mục 2504_0841",
        "images": [DEFAULT_IMAGE]
    },
    # 3. Simple, Internal, Inventory, Allow Negative
    "S2_V1_I2_N2": {
        "name": f"SP Nội Bộ Âm Kho {run_id}",
        "SKU": f"SKU-S2V1I2N2-{run_id}",
        "for_sale": False,
        "has_variants": False,
        "manage_inventory": True,
        "allow_negative": True,
        "batch_name": f"BATCH-NEG-{run_id}",
        "expiry_date": "30/11/2026",
        "total_stock": 10,
        "category": "Danh mục 2504_0841",
        "images": [DEFAULT_IMAGE]
    },
    # 4. Variants, For Sale, No Inventory
    "S1_V2_I1": {
        "name": f"SP Biến Thể Ko Kho {run_id}",
        "SKU": f"SKU-S1V2I1-{run_id}",
        "for_sale": True,
        "has_variants": True,
        "variants_config": [
            {"attribute": "Màu sắc", "values": ["Đỏ", "Xanh"]}
        ],
        "manage_inventory": False,
        "category": "Danh mục 2504_0841",
        "images": [DEFAULT_IMAGE]
    },
    # 5. Variants, For Sale, Inventory, No Negative (4 Variants: 2x2)
    "S1_V2_I2_N1": {
        "name": f"SP Biến Thể 4 Dòng {run_id}",
        "SKU": f"SKU-VAR4-{run_id}",
        "for_sale": True,
        "note": f"NOTE-S2V2I2N2-{run_id}",
        "bar_code": f"BARCODE-S2V2I2N2-{run_id}",
        "has_variants": True,
        "variants_config": [
            {"attribute": "Color", "values": ["Black", "Red"]},
            {"attribute": "Gender", "values": ["Male", "Female"]}
        ],
        "manage_inventory": True,
        "allow_negative": True,
        "batch_name": f"LOT-V4-{run_id}",
        "expiry_date": "31/12/2026",
        "total_stock": [10, 20, 30, 40],
        "wholesale_prices": [100000, 110000, 120000, 130000], # Giá sỉ từng mẫu
        "sale_prices": [200000, 210000, 220000, 230000],     # Giá lẻ từng mẫu
        "category": "Danh mục 2504_0841",
        "group": "Nhóm 2504_0851",
        "supplier": "Đại lý miền nam",
        "images": [DEFAULT_IMAGE],
        "variant_images": [DEFAULT_IMAGE, DEFAULT_IMAGE, DEFAULT_IMAGE, DEFAULT_IMAGE]
    },
    # 6. Variants, Internal, Inventory, Allow Negative
    "S2_V2_I2_N2": {
        "name": f"SP Biến Thể Nội Bộ {run_id}",
        "SKU": f"SKU-S2V2I2N2-{run_id}",
        "note": f"NOTE-S2V2I2N2-{run_id}",
        "bar_code": f"BARCODE-S2V2I2N2-{run_id}",
        "for_sale": False,
        "has_variants": True,
        "variants_config": [
            {"attribute": "Loại", "values": ["Vip", "Thường"]}
        ],
        "manage_inventory": True,
        "allow_negative": True,
        "batch_name": "BATCH-INT-2026",
        "expiry_date": "15/10/2026",
        "total_stock": 100,
        "category": "Danh mục 2504_0841",
        "images": [DEFAULT_IMAGE]
    }
}

# Alias để tương thích với các file test cũ
PRODUCT_TEST_DATA = {
    "basic_product": PRODUCT_MATRIX_DATA["S1_V1_I1"],
    "inventory_product": PRODUCT_MATRIX_DATA["S1_V1_I2_N1"],
    "batch_expiry_product": PRODUCT_MATRIX_DATA["S2_V1_I2_N2"], # Có thể tùy chỉnh thêm nếu cần
    "variants_product": PRODUCT_MATRIX_DATA["S1_V2_I2_N1"]
}
