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
    {"u": "I only have budget of 500k for investment please recommend some properties with unit type details."}
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
