def get_refund_policy():
    """Get company refund policy"""
    try:
        with open("data/refund-policy.md", "r") as f:
            policy = f.read()
        return {"policy": policy}
    except Exception as e:
        print(f"Error reading refund policy: {e}")
        return {"policy": "Error reading policy"} 