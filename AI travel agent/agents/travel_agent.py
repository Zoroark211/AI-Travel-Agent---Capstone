from graphs.travel_graph import create_travel_graph

class TravelAgent:
    def __init__(self):
        self.graph = create_travel_graph()

    def plan_trip(
        self,
        origin: str,
        destination: str,
        depart_date: str,
        return_date: str = None,
        passengers: int = 1,
        hotel_checkin: str = None,
        hotel_checkout: str = None,
        preferences: str = ""
    ):
        state = {
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "return_date": return_date,
            "passengers": passengers,
            "hotel_checkin": hotel_checkin,
            "hotel_checkout": hotel_checkout,
            "preferences": preferences,
        }

        result_state = self.graph.invoke(state)

        flights = result_state.get("flights", [])
        hotels = result_state.get("hotels", [])
        recommended_places = result_state.get("recommended_places")

        recommended_flight = min(flights, key=lambda f: f.get("price_usd") or 1e9) if flights else None
        recommended_hotel = min(hotels, key=lambda h: h.get("total_price_usd") or 1e9) if hotels else None

        return {
            "recommended": {
                "places": recommended_places,
                "flight": recommended_flight,
                "hotel": recommended_hotel,
            },
            "flights": flights,
            "hotels": hotels
        }
