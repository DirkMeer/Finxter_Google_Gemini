class _SafetySettings:
    """Possible settings: off / low / medium / high."""

    def __init__(self):
        self.categories = [
            "HARM_CATEGORY_HARASSMENT",
            "HARM_CATEGORY_HATE_SPEECH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "HARM_CATEGORY_DANGEROUS_CONTENT",
        ]
        self.levels = {
            "off": "BLOCK_NONE",
            "low": "BLOCK_ONLY_HIGH",
            "medium": "BLOCK_MEDIUM_AND_ABOVE",
            "high": "BLOCK_LOW_AND_ABOVE",
        }

    def _get_settings(self, level):
        return [
            {
                "category": category,
                "threshold": self.levels[level],
            }
            for category in self.categories
        ]
    
    def __getattr__(self, name):
        if name in self.levels:
            return self._get_settings(name)
        raise AttributeError("Possible settings: off / low / medium / high.")
    

safety_settings = _SafetySettings()


if __name__ == "__main__":
    print(safety_settings.off)
    print(safety_settings.low)
    print(safety_settings.medium)
    print(safety_settings.high)
    print(safety_settings.non_existent_setting)