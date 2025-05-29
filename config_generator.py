import uuid
from database import get_db, User

def generate_config(telegram_id: int):
    db = get_db()
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if not user.config_uuid:
        user.config_uuid = str(uuid.uuid4())
        db.commit()
    
    return {
        "vless": f"vless://{user.config_uuid}@vpn.example.com:443?security=tls&sni=example.com#ВашаПодписка",
        "shadowocks": f"ss://aes-256-gcm:{user.config_uuid}@vpn.example.com:8388#Подписка"
    }