import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class HotelAgent:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("Please set OPENAI_API_KEY environment variable.")
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a travel assistant that generates realistic hotel options."),
            ("human",
             "Generate a JSON array of 5 realistic hotels in {destination}.\n"
             "Check-in: {checkin_date}, Check-out: {checkout_date}, Guests: {guests}\n"
             "Preferences: {preferences}\n\n"
             "Each hotel must include: name, address, rating (1-5), price_per_night_usd (integer), "
             "total_price_usd (integer), amenities (list).")
        ])

    def search_hotels(self, destination, checkin_date, checkout_date, guests=1, preferences=""):
        chain = self.prompt | self.llm
        response = chain.invoke({
            "destination": destination,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "guests": guests,
            "preferences": preferences
        })

        # Parse JSON safely
        try:
            hotels = json.loads(response.content)
            if isinstance(hotels, list):
                return hotels
        except Exception:
            return []

        return []
