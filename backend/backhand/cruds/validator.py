from .motivation import Motivation
from .exceptions import InvalidMotivation


class Validator:
    @staticmethod
    def validate(motivation: Motivation):
        errors = []
        errors += Validator.validate_name(motivation)
        errors += Validator.validate_strength(motivation)

        if len(errors) > 0:
            raise InvalidMotivation(errors)
        
    @staticmethod
    def validate_name(motivation: Motivation):
        """ Constrangeri de validare """
        errors = []

        if len(motivation.name) < 3:
            errors.append("Numele nu poate sa fie mai mic de 3 caractere")
        
        if '.' in motivation.name:
            errors.append("Numele nu poate contine caracterul '.'")
        
        return errors

        
    @staticmethod
    def validate_strength(motivation: Motivation):
        """ Constrangeri de validare """
        errors = []
        if motivation.strength < 0:
            errors.append("Strength trebuie sa fie mai mare decat 0")
        
        if motivation.strength > 5:
            errors.append("Strength trebuie sa fie mai mic decat 6")

        return errors

