#GG
class RUT:
    def __init__(self, rut: str):
        self.rut = int(rut.replace('-', '').replace('.', '')[:-1])
        self.verification_digit = RUT.get_verification_digit(self.rut)
        if rut not in self.get_all_ruts():
            raise ValueError("Invalid RUT")

    def get_all_ruts(self):
        ruts = [
            self.get_pretty_rut(),
            f"{self.rut}-{self.verification_digit}",
            f"{self.rut}{self.verification_digit}"
        ]
        return ruts + [rut.replace('K', 'k') for rut in ruts]

    def get_pretty_rut(self):
        return f"{self.rut:,}-{self.verification_digit}".replace(',', '.')

    @staticmethod
    def get_pretty_rut_static(rut: int):
        return f"{rut:,}-{RUT.get_verification_digit(rut)}".replace(',', '.')

    @staticmethod
    def get_verification_digit(rut: int):
        multiplier = 2
        result = 0
        for character in str(rut)[::-1]:
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
