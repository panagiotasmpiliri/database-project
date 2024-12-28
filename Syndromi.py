# Syndromi.py
import sqlite3
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from Melos import *
from PyQt6.QtGui import QColor
class Syndromi:
    table_name = 'ΣΥΝΔΡΟΜΗ'  # Ή το σωστό όνομα πίνακα για τους συνδρομητές

    def __init__(self, parent):
        self.parent = parent
        self.table = None
        self.table_shown = False
        self.Buttonstylesheet = self.load_stylesheet("Buttonstyle.txt")
        self.backButton = QPushButton("Επιστροφή")
        self.backButton.setStyleSheet(self.Buttonstylesheet)
        self.backButton.clicked.connect(self.go_back)

    def load_stylesheet(self, style):
        try:
            with open(style, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            return None
    def show_table(self):
        if self.table_shown:
            self.table.setParent(None)  # Αφαιρούμε τον πίνακα αν έχει εμφανιστεί ήδη
            self.table_shown = False
            
        self.table = QTableWidget()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        conn.close()

        # Αν δεν υπάρχουν δεδομένα, δείχνουμε μήνυμα
        if not rows:
            QMessageBox.warning(self.parent, "Προσοχή", "Δεν υπάρχουν συνδρομητές.")
            return

        # Ρύθμιση του πίνακα
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(rows[0]))  # Ο αριθμός των στηλών είναι το μέγεθος της πρώτης γραμμής
        self.table.setHorizontalHeaderLabels(["ID", "Όνομα", "Ημερομηνία Εγγραφής", "Άλλες Στήλες"])  # Εξαρτάται από τις στήλες της βάσης δεδομένων

        # Προσθήκη των δεδομένων στον πίνακα
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


        layout = self.parent.tabSyndromi.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.parent.tabSyndromi.setLayout(layout)

        layout.addWidget(self.table)
        layout.addWidget(self.backButton)
        self.table_shown = True


    def go_back(self):
        if self.table_shown:
            self.table.setParent(None)
            self.backButton.setParent(None)
            self.table_shown = False

            # Καθαρισμός του layout του tabMeli
            layout = self.parent.tabSyndromi.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            # Ενεργοποίηση του κουμπιού "Πίνακας Μελών"
            self.parent.buttonSyndromh.setEnabled(True)

class MelosPlironeiSyndromi(Syndromi,Melos):
    table_name='ΜΕΛΟΣ_ΠΛΗΡΩΝΕΙ_ΣΥΝΔΡΟΜΗ'
    def __init__(self,parent):
        Syndromi.__init__(self,parent)
        Melos.__init__(self,parent)
    
    def go_back(self):
        if self.table_shown:
            self.table.setParent(None)
            self.backButton.setParent(None)
            self.table_shown = False

            # Καθαρισμός του layout του tabMeli
            layout = self.parent.tabSyndromi.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            # Ενεργοποίηση του κουμπιού "Πίνακας Μελών"
            self.parent.buttonPliromon.setEnabled(True)
    def show_table(self):
        query = (f"""SELECT "{Melos.table_name}"."μητρώο_μέλους",
        "{Melos.table_name}"."όνομα",
        "{Melos.table_name}"."επώνυμο",
        "{Syndromi.table_name}"."τρόπος πληρωμής",
        "{Syndromi.table_name}"."πακέτο συνδρομής",20*(
        0.8*("{self.table_name}"."κωδικός συνδρομής"=1 OR "{self.table_name}"."κωδικός συνδρομής"=6) +
        0.7*("{self.table_name}"."κωδικός συνδρομής"=2 OR "{self.table_name}"."κωδικός συνδρομής"=7) +
        1.1*("{self.table_name}"."κωδικός συνδρομής"=3 OR "{self.table_name}"."κωδικός συνδρομής"=8) +
        0.6*("{self.table_name}"."κωδικός συνδρομής"=4 OR "{self.table_name}"."κωδικός συνδρομής"=9) +
        1*("{self.table_name}"."κωδικός συνδρομής"=5 OR "{self.table_name}"."κωδικός συνδρομής"=10))
        AS "ποσό",
        "{self.table_name}"."ημερομηνία πληρωμής"
    FROM 
        "{self.table_name}"
    JOIN 
        "{Melos.table_name}"
    ON 
        "{Melos.table_name}"."μητρώο_μέλους" = "{self.table_name}"."μητρώο_μέλους"
    JOIN 
        "{Syndromi.table_name}"
    ON 
        "{Syndromi.table_name}"."κωδικός συνδρομής" = "{self.table_name}"."κωδικός συνδρομής"
    ORDER BY 
        CAST(SUBSTR("{self.table_name}"."ημερομηνία πληρωμής", 4, 4) AS INTEGER) DESC,
        CAST(SUBSTR("{self.table_name}"."ημερομηνία πληρωμής", 1, 2) AS INTEGER) DESC   
""")

        if self.table_shown:
            self.table.setParent(None)  # Αφαιρούμε τον πίνακα αν έχει εμφανιστεί ήδη
            self.table_shown = False

    # Δημιουργούμε έναν νέο πίνακα
        self.table = QTableWidget()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Ρυθμίσεις του πίνακα
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(8)  # 7 στήλες (συμπεριλαμβανομένων Διαγραφή και Ενημέρωση)
        self.table.setHorizontalHeaderLabels([
            "Μητρώο Μέλους", "Όνομα", "Επώνυμο", "Τρόπος Πληρωμής",
            "Πακέτο Συνδρομής", "Ποσό", "Ημερομηνία Πληρωμής", "Διαγραφή"]
        )

        # Γεμίζουμε τον πίνακα με δεδομένα
        for row, row_data in enumerate(rows):
            for column, value in enumerate(row_data):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))

            # Δημιουργία κουμπιού για Διαγραφή
            delete_button = QPushButton("Διαγραφή")
            delete_button.setStyleSheet(self.Buttonstylesheet)
            delete_button.clicked.connect(lambda checked, row=row: self.delete_entry(row))
            self.table.setCellWidget(row, 7, delete_button)  


        layout = self.parent.tabSyndromi.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.parent.tabSyndromi.setLayout(layout)

        layout.addWidget(self.table)
        layout.addWidget(self.backButton)
        self.table_shown = True

        # Δημιουργία και σύνδεση του κουμπιού για προσθήκη νέας εγγραφής
        self.addButton = QPushButton("Προσθήκη Πληρωμής")
        self.addButton.setStyleSheet(self.Buttonstylesheet)
        self.addButton.clicked.connect(self.add_subscription)
        layout.addWidget(self.addButton)
        self.debtsButton = QPushButton("Πίνακας Οφειλών")
        self.debtsButton.setStyleSheet(self.Buttonstylesheet)
        self.debtsButton.clicked.connect(self.show_debts_table)
        layout.addWidget(self.debtsButton)

    def delete_entry(self, row):
        # Υλοποίηση διαγραφής εγγραφής από τη βάση και το UI
        pass

    def add_subscription(self):
        # Υλοποίηση προσθήκης νέας εγγραφής στη βάση και το UI
        pass
    def show_debts_table(self):
        self.backButton = QPushButton("Επιστροφή")
        self.backButton.setStyleSheet(self.Buttonstylesheet)
        self.backButton.clicked.connect(self.go_back)
        query = (f"""SELECT "{Melos.table_name}"."μητρώο_μέλους",
                        "{Melos.table_name}"."όνομα",
                        "{Melos.table_name}"."επώνυμο",
                        "{Syndromi.table_name}"."τρόπος πληρωμής",
                        "{Syndromi.table_name}"."πακέτο συνδρομής",
                        20*(
                            0.8*("{self.table_name}"."κωδικός συνδρομής"=1 OR "{self.table_name}"."κωδικός συνδρομής"=6) +
                            0.7*("{self.table_name}"."κωδικός συνδρομής"=2 OR "{self.table_name}"."κωδικός συνδρομής"=7) +
                            1.1*("{self.table_name}"."κωδικός συνδρομής"=3 OR "{self.table_name}"."κωδικός συνδρομής"=8) +
                            0.6*("{self.table_name}"."κωδικός συνδρομής"=4 OR "{self.table_name}"."κωδικός συνδρομής"=9) +
                            1*("{self.table_name}"."κωδικός συνδρομής"=5 OR "{self.table_name}"."κωδικός συνδρομής"=10)
                        ) AS "ποσό",
                        MAX("{self.table_name}"."ημερομηνία πληρωμής") AS "τελευταία πληρωμή"
                    FROM "{self.table_name}"
                    JOIN "{Melos.table_name}"
                    ON "{Melos.table_name}"."μητρώο_μέλους" = "{self.table_name}"."μητρώο_μέλους"
                    JOIN "{Syndromi.table_name}"
                    ON "{Syndromi.table_name}"."κωδικός συνδρομής" = "{self.table_name}"."κωδικός συνδρομής"
                    GROUP BY "{Melos.table_name}"."μητρώο_μέλους",
                            "{Melos.table_name}"."όνομα",
                            "{Melos.table_name}"."επώνυμο",
                            "{Syndromi.table_name}"."τρόπος πληρωμής",
                            "{Syndromi.table_name}"."πακέτο συνδρομής"
                    ORDER BY 
                        CAST(SUBSTR(MAX("{self.table_name}"."ημερομηνία πληρωμής"), 4, 4) AS INTEGER) DESC,
                        CAST(SUBSTR(MAX("{self.table_name}"."ημερομηνία πληρωμής"), 1, 2) AS INTEGER) DESC
                """)

        # Καθαρισμός του layout του tabSyndromi
        layout = self.parent.tabSyndromi.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Δημιουργούμε έναν νέο πίνακα
        self.table = QTableWidget()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Ρυθμίσεις του πίνακα
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(8)  # 8 στήλες
        self.table.setHorizontalHeaderLabels([
            "Μητρώο Μέλους", "Όνομα", "Επώνυμο", "Τρόπος Πληρωμής",
            "Πακέτο Συνδρομής", "Ποσό", "Τελευταία Πληρωμή", "Κατάσταση"
        ])

        # Χρωματισμός γραμμών και συμπλήρωση δεδομένων
        from datetime import datetime
        today = datetime.today().strftime("%m-%Y")  # Λήψη τρέχοντος μήνα και έτους (π.χ., "09-2024")

        for row_idx, row_data in enumerate(rows):
            has_paid = row_data[-1].endswith(today)  # Έλεγχος αν η ημερομηνία πληρωμής είναι αυτόν τον μήνα
            color = QColor("green") if has_paid else QColor("red")  # Χρήση QColor για το χρώμα

            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setBackground(color)  # Ορίζει το χρώμα του κελιού
                self.table.setItem(row_idx, col_idx, item)

            # Κατάσταση: "Πληρωμένο" ή "Οφειλή"
            status = "Πληρωμένο" if has_paid else "Οφειλή"
            status_item = QTableWidgetItem(status)
            status_item.setBackground(color)
            self.table.setItem(row_idx, 7, status_item)  # Στήλη Κατάσταση

        # Προσθήκη του πίνακα και του κουμπιού "Επιστροφή"
        layout.addWidget(self.table)

        # Προσθέτουμε ξανά το κουμπί "Επιστροφή"
        layout.addWidget(self.backButton)

        self.table_shown = True
