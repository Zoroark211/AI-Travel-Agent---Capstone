from langgraph.graph import StateGraph, END

def create_travel_graph():
    from agents.flight_agent import FlightAgent
    from agents.hotel_agent import HotelAgent
    from langchain_openai import ChatOpenAI
    import json

    flight_agent = FlightAgent()
    hotel_agent = HotelAgent()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    def get_flights(state):
        flights = flight_agent.search_flights(
            state["origin"], state["destination"], state["depart_date"],
            state.get("return_date"), state.get("passengers", 1),
            state.get("preferences", "")
        )
        state["flights"] = flights
        return state

    def get_hotels(state):
        hotels = hotel_agent.search_hotels(
            state["destination"], state["hotel_checkin"], state["hotel_checkout"],
            state.get("passengers", 1), state.get("preferences", "")
        )
        state["hotels"] = hotels
        return state

    def recommend(state):
        best_flight = min(state.get("flights", []), key=lambda f: f.get("price_usd", 999999), default=None)
        best_hotel = min(state.get("hotels", []), key=lambda h: h.get("total_price_usd", 999999), default=None)

        q = f"""
        Return ONLY valid JSON.
        Suggest one must-see attraction in {state['destination']}.
        Format:
        {{
        "place": "Eiffel Tower"
        }}
        """
        attraction = {"place": "Unknown"}
        try:
            resp = llm.invoke(q)

            raw_text = resp.content if isinstance(resp.content, str) else str(resp.content)

            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1:
                attraction = json.loads(raw_text[start:end+1])

        except Exception as e:
            print("LLM parsing failed:", e)

        state["recommended"] = {
            "place": attraction.get("place", "Unknown"),
            "flight": best_flight,
            "hotel": best_hotel
        }
        return state


    graph = StateGraph(dict)

    graph.add_node("flights", get_flights)
    graph.add_node("hotels", get_hotels)
    graph.add_node("recommend", recommend)

    graph.set_entry_point("flights")
    graph.add_edge("flights", "hotels")
    graph.add_edge("hotels", "recommend")
    graph.add_edge("recommend", END)

    return graph.compile()
