from PyQt6.QtCore import QObject, pyqtSignal

class SignalBus(QObject):
    inventory_updated = pyqtSignal()

signal_bus = SignalBus()