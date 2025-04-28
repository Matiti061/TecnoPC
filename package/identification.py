class Identification:
    def __init__(self, identification: str):
        self._identification = int(identification.replace('-', '').replace('.', '')[:-1])
        self._verification_digit = self._get_verification_digit()
        if identification not in self._get_all_identifications():
            raise ValueError("Invalid identification")

    def _get_all_identifications(self):
        identifications = [
            self._get_pretty_identification(),
            f"{self.identification}-{self._verification_digit}",
            f"{self.identification}{self._verification_digit}"
        ]
        return identifications

    def _get_pretty_identification(self):
        return f"{self.identification:,}-{self._verification_digit}".replace(',', '.')

    def _get_verification_digit(self):
        multiplier = 2
        result = 0
        for character in str(self._identification)[::-1]:
            if multiplier > 7:
                multiplier = 2
            result += int(character) * multiplier
            multiplier += 1
        result = 11 - result % 11
        if result == 10:
            return 'K'
        if result == 11:
            return '0'
        return str(result)

    @property
    def identification(self):
        return self._identification
