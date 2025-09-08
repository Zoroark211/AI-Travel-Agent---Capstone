from dotenv import load_dotenv
import gradio as gr
import json
from agents.travel_agent import TravelAgent

load_dotenv()

agent = TravelAgent()

def plan_trip_ui(origin, destination, depart_date, return_date,
                 passengers, checkin_date, checkout_date, preferences):
    try:
        result = agent.plan_trip(
            origin=origin,
            destination=destination,
            depart_date=depart_date,
            return_date=return_date,
            passengers=int(passengers or 1),
            hotel_checkin=checkin_date,
            hotel_checkout=checkout_date,
            preferences=preferences
        )

        # Summary
        recommended = result.get("recommended", {})
        summary_lines = []

        if recommended.get("place"):
            summary_lines.append(f"Recommended place to visit: **{recommended['place']}**")

        flight = recommended.get("flight")
        if flight:
            summary_lines.append(
                f"Best flight: {flight.get('airline')} {flight.get('flight_number')} "
                f"({flight.get('depart_time')} → {flight.get('arrive_time')}), "
                f"${flight.get('price_usd')}"
            )

        hotel = recommended.get("hotel")
        if hotel:
            summary_lines.append(
                f"Best hotel: {hotel.get('name')} ({hotel.get('rating')}⭐), "
                f"${hotel.get('total_price_usd')} total"
            )

        summary = "\n".join(summary_lines) if summary_lines else "No recommendations found."
        json_output = json.dumps(result, indent=2)

        return summary, json_output

    except Exception as e:
        return f"Error: {e}", "{}"


with gr.Blocks(title="AI Travel Planner") as demo:
    gr.Markdown("AI Travel Planner\nPlan your next trip with AI-powered recommendations.")

    with gr.Row():
        origin = gr.Textbox(label="Origin (e.g. SFO)")
        destination = gr.Textbox(label="Destination (e.g. LAX)")

    with gr.Row():
        depart_date = gr.Textbox(label="Departure Date (YYYY-MM-DD)")
        return_date = gr.Textbox(label="Return Date (YYYY-MM-DD, optional)")

    with gr.Row():
        passengers = gr.Number(label="Passengers", value=1, precision=0)
        checkin_date = gr.Textbox(label="Hotel Check-in (YYYY-MM-DD)")
        checkout_date = gr.Textbox(label="Hotel Check-out (YYYY-MM-DD)")

    preferences = gr.Textbox(label="Preferences (e.g. budget, luxury, non-stop flight)")

    submit_btn = gr.Button("Plan My Trip")

    with gr.Row():
        summary_output = gr.Markdown(label="Summary")
    json_output = gr.JSON(label="Full JSON Output")

    submit_btn.click(
        fn=plan_trip_ui,
        inputs=[origin, destination, depart_date, return_date,
                passengers, checkin_date, checkout_date, preferences],
        outputs=[summary_output, json_output]
    )


if __name__ == "__main__":
    demo.launch()
