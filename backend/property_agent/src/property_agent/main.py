#!/usr/bin/env python
from flows.flow import RouterFlow

def kickoff():
    flow = RouterFlow()
    flow.kickoff()

def plot():
    flow = RouterFlow()
    flow.plot()

if __name__ == "__main__":
    inputs = [
    {"u": "Hi, I'm looking for a property suitable for a family of 3 with maximum budget of RM 800,000."},
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
