
import streamlit as st
import random
class Field:
    def __init__(self):
        self.board = [[] for _ in range(9)]

    def add_figure_to_field(self, index, player_id, current_round):
        self.board[index].append([player_id, current_round])

    def remove_last_from_field(self, index):
        self.board[index].pop()

    def remove_figure_from_field(self, index, player_id, current_round):
        if ([player_id, current_round] in self.board[index]):
            self.board[index].remove([player_id, current_round])

    def display_field(self):
        self.sort_fields()
        return [' '.join(str(player) for [player,_] in field) if field else 'leer' for field in self.board]

    def sort_fields(self): 
        [field.sort() for field in self.board]

    def calculate_customers(self, min_customers=2, max_customers=7):
        result = []

        for field_index, field in enumerate(self.board):
            if not field:  # Wenn das Feld leer ist, überspringen
                continue

            total_customers = random.randint(min_customers, max_customers)
            
            player_weights = {}
            for player_info in field:
                player, round_entered = player_info
                duration = st.session_state.current_round - round_entered
                weight = duration * 1.5  # Gewichtung
                if player in player_weights:
                    player_weights[player] = max(player_weights[player], weight)
                else:
                    player_weights[player] = weight

            # Gesamtes Gewicht aller Spieler berechnen
            total_weight = sum(player_weights.values())

            # Kunden proportional zu den Gewichten auf Spieler verteilen
            for player, weight in player_weights.items():
                if total_weight > 0:
                    player_customers = int(total_customers * (weight / total_weight))
                else:
                    player_customers = 0

                result.append({
                    "field": field_index + 1,
                    "player": player,
                    "customers": player_customers
                })

        return result

    def show_customers_by_player(self, results):
        grouped = {}

        # Ergebnisse nach Spielern gruppieren
        for entry in results:
            player = entry["player"]
            field = entry["field"]
            customers = entry["customers"]

            if player not in grouped:
                grouped[player] = []
            
            grouped[player].append({"field": field, "customers": customers})

        # Textformat erstellen
        text_output = []
        for player, fields in sorted(grouped.items()):
            text_output.append(f"Spieler {player}:")
            for field_entry in sorted(fields, key=lambda x: x["field"]):
                text_output.append(f"    Feld {field_entry['field']}: {field_entry['customers']} Kunden")
            text_output.append("")  # Leerzeile zwischen Spielern

        return "\n".join(text_output)


    def show(self):
        print(self.board)