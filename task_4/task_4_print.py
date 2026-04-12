MIN_FIELD_LENGTH = 7
MIN_TYPE_LENGTH = 6
MIN_DEFAULT_LENGTH = 9


def calc_column_length(data: dict):
    """Нахождение максимальной длины для каждого поля среди всех классов"""
    max_lengths = [
        max(len(row[i]) for rows in data.values() for row in rows) + 2 for i in range(3)
    ]

    field_len = (
        max_lengths[0] if max_lengths[0] >= MIN_FIELD_LENGTH else MIN_FIELD_LENGTH
    )
    type_len = max_lengths[1] if max_lengths[1] >= MIN_TYPE_LENGTH else MIN_TYPE_LENGTH
    default_len = (
        max_lengths[2] if max_lengths[2] >= MIN_DEFAULT_LENGTH else MIN_DEFAULT_LENGTH
    )

    return field_len, type_len, default_len


def print_models_info(data: dict) -> None:
    """Вывод информации по каждому классу"""
    field_len, type_len, default_len = calc_column_length(data)

    separator = (
        "+" + "-" * field_len + "+" + "-" * type_len + "+" + "-" * default_len + "+"
    )

    for key, value in data.items():
        print(f"Model: {key}")
        print(separator)

        print(
            "|"
            + " Field"
            + " " * (field_len - 6)
            + "|"
            + " Type"
            + " " * (type_len - 5)
            + "|"
            + " Default"
            + " " * (default_len - 8)
            + "|"
        )
        print(separator)

        for v in value:
            print(
                "|"
                + f" {v[0]}"
                + " " * (field_len - len(v[0]) - 1)
                + "|"
                + f" {v[1]}"
                + " " * (type_len - len(v[1]) - 1)
                + "|"
                + f" {v[2]}"
                + " " * (default_len - len(v[2]) - 1)
                + "|"
            )
        print(separator, "\n")

    return None


# Model: UserSchema
# +-----------------+-------------------+---------+
# | Field           | Type              | Default |
# +-----------------+-------------------+---------+
# | id              | UUID              | —       |
# | phone           | int               | —       |
# | birthday        | Optional[str]     | None    |
# | profile_data    | Optional[dict]    | None    |
# +-----------------+-------------------+---------+
#
# Model: ReceptionSchema
# +-----------------+-------------------+---------+
# | ...             | ...               | ...     |
# +-----------------+-------------------+---------+
