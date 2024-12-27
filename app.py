import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.uic import loadUi

# Αρχικοί imports
# Από τη στιγμή που θα κάνουμε καθυστερημένα imports για τις κλάσεις που χρειάζονται
# δεν χρειάζεται να εισάγουμε τίποτα από πάνω

class Main(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("untitled.ui", self)
        self.melos = None  # Αρχικοποιούμε το στιγμιότυπο της κλάσης Meli
        self.playerInTeam = None
        self.playerNoInTeam = None
        self.playerPaid = None
        self.subscription = None  # Προσθήκη της νέας μεταβλητής για το συνδρομητή

        # Συνδέουμε τα κουμπιά με τις αντίστοιχες μεθόδους
        self.buttonTableMeli.clicked.connect(self.show_member_table)
        self.buttonTablePaiktis.clicked.connect(self.show_teampaiktis_table)
        self.buttonTableNoInTeam.clicked.connect(self.show_no_teampaiktis_table)
        self.buttonTablePaidPaiktis.clicked.connect(self.show_paid_paiktis_table)
        self.buttonSyndromh.clicked.connect(self.show_subscription_table)  # Νέα σύνδεση για το κουμπί συνδρομητών

    def show_member_table(self):
        from Melos import Melos  # Καθυστερημένη εισαγωγή
        if self.melos is None:
            self.melos = Melos(self)
        self.melos.show_table()

    def show_teampaiktis_table(self):
        from Paiktis import TeamPaiktis  # Καθυστερημένη εισαγωγή
        if self.playerInTeam is None:
            self.playerInTeam = TeamPaiktis(self)
        self.playerInTeam.show_table()

    def show_no_teampaiktis_table(self):
        from Paiktis import ΝοTeamPaiktis  # Καθυστερημένη εισαγωγή
        if self.playerNoInTeam is None:
            self.playerNoInTeam = ΝοTeamPaiktis(self)
        self.playerNoInTeam.show_table()

    def show_paid_paiktis_table(self):
        from Paiktis import PaiktisAmeivomenos  # Καθυστερημένη εισαγωγή
        if self.playerPaid is None:
            self.playerPaid = PaiktisAmeivomenos(self)
        self.playerPaid.show_table()

    def show_subscription_table(self):
        from Syndromi import Syndromi  # Καθυστερημένη εισαγωγή της κλάσης Syndromi
        if self.subscription is None:
            self.subscription = Syndromi(self)
        self.subscription.show_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
