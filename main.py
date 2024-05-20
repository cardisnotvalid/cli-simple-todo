import argparse

from database import db_handler


@db_handler
def print_db(db):
    todo_list = db.get_all()

    max_id_length = max(map(lambda t: len(str(t.id)), todo_list))
    max_name_length = max(map(lambda t: len(t.name), todo_list))

    header_dict = {
        "#": max_id_length,
        "☐": 1,
        "Name": max_name_length,
        "Created": 19
    }

    header_text = []
    for k, v in header_dict.items():
        header_text.append(str(k).ljust(v))
    print(" | ".join(header_text))

    body_text = []
    for t in todo_list:
        t_checked = "✓" if t.checked else "𐄂"

        row_dict = {
            t.id: max_id_length,
            t_checked: (1,),
            t.name: max_name_length,
            t.created_at: 19
        }
        row_text = []
        for k, v in row_dict.items():
            if isinstance(v, tuple):
                row_text.append(str(k).center(v[0]))
            else:
                row_text.append(str(k).ljust(v))
        body_text.append(" | ".join(row_text))

    print("\n".join(body_text))


@db_handler
def add(db, name, checked):
    db.add(name, checked=checked)


@db_handler
def delete(db, id):
    db.delete(id)


@db_handler
def update(db, id, checked):
    db.update(id, checked)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="sub-command help")

    show_parser = subparsers.add_parser("show", help="Show todo table")
    show_parser.set_defaults(func=lambda args: print_db())

    add_parser = subparsers.add_parser("add", help="Add todo")
    add_parser.add_argument("name", help="Name of todo")
    add_parser.add_argument("--checked", action="store_true", help="Make checked todo")
    add_parser.set_defaults(func=lambda args: add(args.name, checked=args.checked))

    delete_parser = subparsers.add_parser("delete", help="Delete todo")
    delete_parser.add_argument("id", help="Id of todo")
    delete_parser.set_defaults(func=lambda args: delete(args.id))

    update_parser = subparsers.add_parser("update", help="Update todo")
    update_parser.add_argument("id", help="Id of todo")
    update_parser.add_argument("--checked", action="store_true", help="Checked of todo")
    update_parser.set_defaults(func=lambda args: update(args.id, args.checked))

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print_db()
