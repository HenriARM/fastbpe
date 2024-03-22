# TODO: make a Class BPE which does all this encode and decode
# TODO: add types to all functions

def get_top_pair(tokens):
    pairs_count = {}
    for i in range(len(tokens) - 1):
        pair = tokens[i], tokens[i + 1]
        if pair in pairs_count:
            pairs_count[pair] += 1
        else:
            pairs_count[pair] = 1
    sorted_pairs = sorted(pairs_count.items(), key=lambda x: x[1], reverse=True)
    top_pair = sorted_pairs[0][0]
    return top_pair


def merge_pair(tokens, pair, new_token):
    merged = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
            merged.append(new_token)
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return merged


def bpe(tokens, src_vocab_size=256, tgt_vocab_size=260):
    merges = {}
    new_token = src_vocab_size
    while new_token < tgt_vocab_size:
        top_pair = get_top_pair(tokens)
        new_token += 1
        print(f"merging {top_pair} to {new_token}")
        merges[new_token] = top_pair
        tokens = merge_pair(tokens, top_pair, new_token)
    return merges, tokens


def decode(tokens, merges):
    # sort merges by key (highest first)
    merges = dict(sorted(merges.items(), key=lambda x: x[0], reverse=True))
    for new_token, pair in merges.items():
        tokens = [pair if token == new_token else token for token in tokens]
        # flatten
        tokens = [
            x for pair in tokens for x in (pair if isinstance(pair, tuple) else (pair,))
        ]
    return tokens


vocab = [bytes([i]) for i in range(256)]

def dec(ids: list[int]) -> str:
    dec_tokens = b"".join(vocab[idx] for idx in ids)
    text = dec_tokens.decode("utf-8", errors="replace")
    return text
    

def main():
    print(dec([97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107]))
    # TODO: read text from file
    text = "hello my name is henry"

    # TODO: encode function
    
    tokens = text.encode("utf-8")
    tokens = list(map(int, tokens))
    merges, new_tokens = bpe(tokens)
    print(
        "before bpe:",
        len(tokens),
        "after bpe:",
        len(new_tokens),
        "with merges:",
        merges,
    )

    dec_tokens = decode(new_tokens, merges)
    print(text)

    # TODO: assert
    print("encoded:", tokens)
    print("decoded:", dec_tokens)
    # TODO: assert input and output strings


if __name__ == "__main__":
    main()


# TODO: segment subwords (to show as in https://tiktokenizer.vercel.app/)
# TODO: fastBPE
# TODO: add GPT2 tokenizer and GPT4 patterns