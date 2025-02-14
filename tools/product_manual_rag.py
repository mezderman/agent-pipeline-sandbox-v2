def get_product_manual():
    """Get company product manual"""
    try:
        with open("data/product-manual.md", "r") as f:
            manual = f.read()
        return {"manual": manual}
    except Exception as e:
        print(f"Error reading product manual: {e}")
        return {"manual": "Error reading manual"} 