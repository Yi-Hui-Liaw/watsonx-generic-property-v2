#!/usr/bin/env python
from flows.flow import RouterFlow

def kickoff():
    flow = RouterFlow()
    flow.kickoff()


def plot():
    flow = RouterFlow()
    flow.plot()


if __name__ == "__main__":
    # inputs = [
    #     {"u": "Hi, I want to book an appointment."},
    #     {
    #         "a": "Sure, can I get your name, age, gender and insurance?",
    #     },
    #     {
    #         "u": "my name is John Hugh, 26 and I'm a male, for now I dont have insurance.",
    #     },
    #     {
    #         "a": "Can I have your phone number? it is for us to inform you for any updates.",
    #     },
    #     {
    #         "u": "sure my phone number is 0123456789",
    #     },
    #     {
    #         "a": "Can you tell me the health issue you are facing?",
    #     },
    #     {
    #         "u": "My skin is very itchy and flaky. I scratch alot and it starts to irritate",
    #     },
    #     {
    #         "a":"Based on doctor's expertise, I recommend the following doctor for your consultation. They are experienced in treating symptoms like itchy, flaky skin. Here's available doctor: * Dr. Emily Davis (Monday: 11am-12pm, 12pm-1pm, 5pm-6pm)"
    #     },
    #     {
    #         "u": "I prefer 11AM with dr emily",
    #     },
    # ]
    inputs = [
    {"u": "Hi, I'm looking for a property suitable for a family of 3 with maximum budget of Rm 700,000."},
    # {"a": "Sure, can you tell me how many bedrooms you're looking for?"},
    # {"u": "I need at least 3 bedrooms."},
    # {"a": "What is your maximum budget?"},
    # {"u": "My budget is RM 800,000."},
    # {"a": "Do you have any preference for location?"},
    # {"u": "I'm looking for something in the city center."},
    # {"a": "Do you prefer furnished or unfurnished properties?"},
    # {"u": "I prefer a fully furnished apartment."},
    # {"a": "Do you need parking space?"}, 
    # {"u": "Yes, I need parking space."},
    {"a": "Let me find the best properties that fit your preferences."},
    ]
    q = ""
    flow = RouterFlow()

    # Uncomment when you want to test directly from CLI
    # while q != "exit":
    #     q = input()
    #     inputs.append({"u": q})
    result = flow.kickoff(inputs={"inputs": inputs})
        # inputs.append({"a": str(result)})
    print("Flow result:",result)
