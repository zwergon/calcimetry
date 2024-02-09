
models_dict = {
    "LSTM": None,
}


class ModelError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_model(config: dict, input_size, output_size, device):
    kind = config["type"]
    try:
        model = models_dict[kind](input_size, output_size, config)
    except KeyError:
        raise ModelError(f"model {kind} is not handled")

    model = model.to(device=device)
    return model
