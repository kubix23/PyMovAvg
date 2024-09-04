from abc import abstractmethod, ABC


class Indicator(ABC):
    @abstractmethod
    def calculate(self, **kwargs):
        pass


