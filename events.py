import random

#TODO: Ereignisse mit in Customer verechnung einarbeiten

class Event():
    def get_event(self, event_data, game_data, current_round):
        events = event_data["data"]
        drogen = game_data["drogen"]
        lieferanten = game_data["lieferanten"]

        filtered_data = [entry for entry in events if current_round >= entry["min_round"]]

        if not filtered_data:
            return("ERROR")

        texts = [entry["text"] for entry in filtered_data]
        probabilities = [entry["probability"] for entry in filtered_data]

        event = random.choices(texts, weights=probabilities, k=1)[0]

        if "*D*" in event:
            event = event.replace("*D*", random.choice(drogen)["name"])
        
        if "*B*" in event:
            event = event.replace("*B*", str(random.randint(1, 9)))

        if "*S*" in event:
            event = event.replace("*S*", str(random.randint(1,4)))
        
        if "*L*" in event:
            event = event.replace("*L*", random.choice(lieferanten)["name"])
        
        return event
