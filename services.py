from .models import Block


def is_chain_valid():
    blocks = Block.objects.order_by('index')

    for i in range(1, len(blocks)):
        current = blocks[i]
        previous = blocks[i - 1]

        # Check 1: previous hash link
        if current.previous_hash != previous.hash:
            return False

        # Check 2: current hash integrity
        if current.hash != current.calculate_hash():
            return False

    return True


from .models import Block


def get_chain_status():
    blocks = list(Block.objects.order_by('index'))

    for i in range(1, len(blocks)):
        current = blocks[i]
        previous = blocks[i - 1]

        # Check 1: Previous hash mismatch
        if current.previous_hash != previous.hash:
            return {
                "is_valid": False,
                "error": f"Block {current.index} has invalid previous hash.",
                "block": current.index
            }

        # Check 2: Hash mismatch (data tampering)
        if current.hash != current.calculate_hash():
            return {
                "is_valid": False,
                "error": f"Block {current.index} data has been tampered.",
                "block": current.index
            }

    return {
        "is_valid": True,
        "error": None,
        "block": None
    }
