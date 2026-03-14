TRANSLATIONS = {
    "delivery": {
        "ru": "Доставка",
        "kz": "Жеткізу",
        "uz": "Yetkazib berish",
    },
    "pickup": {
        "ru": "Самовывоз",
        "kz": "Өзі алып кету",
        "uz": "O'zi olib ketish",
    },
    "order_received": {
        "ru": "Заказ принят",
        "kz": "Тапсырыс қабылданды",
        "uz": "Buyurtma qabul qilindi",
    },
    "in_progress": {
        "ru": "В процессе",
        "kz": "Өңделуде",
        "uz": "Jarayonda",
    },
    "delivered": {
        "ru": "Доставлено",
        "kz": "Жеткізілді",
        "uz": "Yetkazildi",
    },
}


def translate(key, lang="kk"):
    return TRANSLATIONS.get(key, {}).get(lang, key)