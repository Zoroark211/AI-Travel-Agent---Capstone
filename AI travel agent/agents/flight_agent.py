from amadeus import Client, ResponseError
from config import AMADEUS_API_KEY, AMADEUS_API_SECRET

class FlightAgent:
    def __init__(self):
        self.amadeus = Client(
            client_id = AMADEUS_API_KEY,
            client_secret = AMADEUS_API_SECRET
        )

    def search_flights(self, origin, destination, depart_date, return_date=None, passengers=1, preferences=""):
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=depart_date,
                returnDate=return_date,
                adults=passengers,
                max=5
            )
            return [offer for offer in response.data]
        except ResponseError as e:
            print(e)
            return []