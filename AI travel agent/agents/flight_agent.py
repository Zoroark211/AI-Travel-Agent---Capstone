import json
from amadeus import Client
from config import AMADEUS_API_KEY, AMADEUS_API_SECRET
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class FlightAgent:
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a travel assistant that generates realistic flight options."),
            ("human", 
             "Generate a JSON array of 5 realistic flight options from {origin} to {destination}.\n"
             "Departure date: {depart_date}\n"
             "Return date: {return_date}\n"
             "Passengers: {passengers}\n"
             "Preferences: {preferences}\n\n"
             "Each flight must include: airline, flight_number, depart_time, arrive_time, duration, "
             "stops, price_usd (integer).")
        ])

    def search_flights(self, origin, destination, depart_date, return_date=None, passengers=1, preferences=""):
        chain = self.prompt | self.llm
        response = chain.invoke({
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "return_date": return_date or "N/A",
            "passengers": passengers,
            "preferences": preferences
        })

        # Parse JSON safely
        try:
            flights = json.loads(response.content)
            if isinstance(flights, list):
                return flights
        except Exception:
            return []

        return []
