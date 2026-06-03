from cafelibro.storage import load_data, save_data


def register_member(member_id: str, name: str) -> dict:
    data = load_data()
    if any(m["id"] == member_id for m in data["members"]):
        raise ValueError(f"A member with id '{member_id}' already exists.")
    member = {"id": member_id, "name": name}
    data["members"].append(member)
    save_data(data)
    return member