#!/usr/bin/env python
import os
os.environ["OTEL_SDK_DISABLED"] = "true"

from flows.flow import RouterFlow

def kickoff():
    flow = RouterFlow()
    flow.kickoff()

def plot():
    flow = RouterFlow()
    flow.plot()

if __name__ == "__main__":
    inputs = [
    {"u": "I like to play golf. Recommend property."}
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
