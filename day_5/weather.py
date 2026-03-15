def get_temperature():
    # In real life, this would call a weather API
    pass

class WeatherAlertService:
    def get_alert(self):
        temp = get_temperature()
        if temp >= 40:
            return "HIGH"
        elif temp <= 10:
            return "LOW"
        else:
            return "NORMAL"