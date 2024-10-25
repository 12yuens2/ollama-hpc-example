import csv
import json
import os
from argparse import ArgumentParser

import ollama

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDATA_PATH = os.path.join(main_dir, "data/pizza_types.csv")
OUTDATA_PATH = os.path.join(main_dir, "data/pizza_scored.csv")

MODEL_CHOICE = "llama3.2:1b"  # The smallest llama model


def get_args():
    """Get the arguments from the command line
    Gets the values
    --host_port: The host and port of the llama server
    --model_name: The name of the llama model to use
    """
    parser = ArgumentParser(description="Run ollama to score pizzas")

    # The default port is 11434
    parser.add_argument(
        "--host_port",
        type=str,
        default="11434",
        help="The host and port of the llama server",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default=MODEL_CHOICE,
        help="The name of the llama model to use",
    )

    return parser.parse_args()


def get_pizza_score(client, pizza_name):
    """Run the model to get the score of a pizza.
    This is always processes with a josn format.
    This works well for the llama3 models but might not for others.

    Args:
        client (ollama.Client): The llama client to use
        pizza_name (str): The name of the pizza to score

    Returns:
        score (float): The score of the pizza
        reason (str): The reason for the score
    """
    responce = client.chat(
        MODEL_CHOICE,
        messages=[
            {"role": "user", "content": "I want to score some pizzas."},
            {
                "role": "assistant",
                "content": (
                    "Excellent! I will score them out of ten."
                    "I will provide a JSON file."
                    "The JSON file will have the pizza name under 'type', "
                    "the reason for the score under 'reason', "
                    "and the score under 'score'."
                ),
            },
            {"role": "user", "content": f"The first pizza is a {pizza_name}."},
        ],
        options={"Temperature": 0.5},  # This option can pass many settings
        format="json",  # JSONs are easier to work with in Python
        keep_alive=60,  # How long the model should be kept in memory after the call
    )

    given_json = json.loads(responce["message"]["content"])

    if "score" not in given_json:
        given_json["score"] = 0

    if "reason" not in given_json:
        given_json["reason"] = "No reason given"

    return given_json["score"], given_json["reason"]


def get_model(model_name):
    """Ollama Pull downloads the model if it is not found
    This command is the same as running `ollama pull model_name` in the terminal
    """
    if model_name not in [mod["name"] for mod in ollama.list()["models"]]:
        print("Model not found. Trying to download...")
        ollama.pull(model_name)


def main():
    # Get the Host Port and Model Name
    args = get_args()

    # Get the model - probably best to not do this on the compute node
    # get_model(args.model_name)

    # A llama client is doesn't need to be created as `ollama.call` will
    # work without it. I believe the client option allows the host option
    # to be set which might be needed for some setups.
    ollama_client = ollama.Client(host=f"localhost:{args.host_port}")

    pizza_numbers = []
    pizza_names = []
    pizza_scores = []
    pizza_reasons = []

    with open(INDATA_PATH, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            p_score, p_reason = get_pizza_score(ollama_client, row[1])
            pizza_numbers.append(row[0])
            pizza_names.append(row[1])
            pizza_scores.append(p_score)
            pizza_reasons.append(p_reason.replace(",", ""))

    with open(OUTDATA_PATH, "w") as outfile:

        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["Number", "Name", "Score", "Reason"])

        for i in range(len(pizza_numbers)):
            csv_writer.writerow(
                [pizza_numbers[i], pizza_names[i], pizza_scores[i], pizza_reasons[i]]
            )


if __name__ == "__main__":
    main()
