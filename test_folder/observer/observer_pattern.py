
import zope.interface


class IObserver(zope.interface.Interface):
    x = zope.interface.Attribute("foo")

    def update(self):
        pass


class Observer:
    def __init__(self) -> None:
        self.obs = []

    def add_observer(self, obs):
        self.obs.append(obs)

    def remove_observer(self, obs):
        self.obs.pop(obs)

    def notify_observers(self):
        for item in self.obs:
            item.update()


class DataSource(Observer):
    def __init__(self) -> None:
        self.value = 0
        self.obs = []

    def set_value(self, value):
        self.value = value
        self.notify_observers()

    def get_value(self):
        return self.value


@zope.interface.implementer(IObserver)
class Chart:
    def __init__(self, data_source) -> None:
        self.__data_source = data_source

    def update(self):
        print('Chart got updated', self.__data_source.get_value())


@zope.interface.implementer(IObserver)
class SpreadSheet:
    def __init__(self, data_source) -> None:
        self.__data_source = data_source

    def update(self):
        print('SpreadSheet got notified', self.__data_source.get_value())


if __name__ == '__main__':
    data_source = DataSource()
    sheet1 = SpreadSheet(data_source)
    sheet2 = SpreadSheet(data_source)
    chart = Chart(data_source)

    data_source.add_observer(sheet1)
    data_source.add_observer(sheet2)
    data_source.add_observer(chart)

    data_source.set_value('1')
    data_source.set_value('2')
