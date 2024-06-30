GEMINI_FLASH = "gemini-1.5-flash"
GEMINI_PRO = "gemini-1.5-pro"

COST_IN_CENTS = {
    GEMINI_FLASH: {
        'input': 35,
        'output': 105,
    },
    GEMINI_PRO: {
        'input': 350,
        'output': 1050,
    },
}


def print_cost_in_dollars(usage_metadata, model_name):
    input_tokens = usage_metadata.prompt_token_count
    output_tokens = usage_metadata.candidates_token_count

    input_cost_cents_per_token = COST_IN_CENTS[model_name]['input'] / 1_000_000.0
    output_cost_cents_per_token = COST_IN_CENTS[model_name]['output'] / 1_000_000.0

    total_cost_in_cents = (input_tokens * input_cost_cents_per_token) + (output_tokens * output_cost_cents_per_token)
    total_cost_in_dollars = total_cost_in_cents / 100.0

    print(f"Cost: ${total_cost_in_dollars:.9f}")


if __name__ == "__main__":
    class TestUsageMetadata:
        def __init__(self, prompt_token_count, candidates_token_count):
            self.prompt_token_count = prompt_token_count
            self.candidates_token_count = candidates_token_count
            
    usage_metadata = TestUsageMetadata(1_000_000, 0)
    print_cost_in_dollars(usage_metadata, GEMINI_FLASH)
    print_cost_in_dollars(usage_metadata, GEMINI_PRO)
    usage_metadata = TestUsageMetadata(0, 1_000_000)
    print_cost_in_dollars(usage_metadata, GEMINI_FLASH)
    print_cost_in_dollars(usage_metadata, GEMINI_PRO)