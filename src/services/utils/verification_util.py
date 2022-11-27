def remove_duplicates_from_intput(docs_list: list) -> list:
    return [dict(t) for t in [tuple(d.items()) for d in docs_list]]

