import random


def generate_nickname() -> str:
    noun_list = []
    with open("utils/korean_noun.txt", "r", encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            noun_list.append(line.strip())

    return random.choice(noun_list)


def generate_color() -> str:
    colors = [
        "#FF0000",  # Red
        "#FFA500",  # Orange
        "#FFFF00",  # Yellow
        "#008000",  # Green
        "#0000FF",  # Blue
        "#4B0082",  # Indigo
        "#EE82EE",  # Violet
        "#FFC0CB",  # Pink
        "#00FFFF",  # Cyan
        "#800080",  # Purple
        "#FF6347",  # Tomato
        "#008080",  # Teal
        "#8B0000",  # Dark Red
        "#00FF7F",  # Spring Green
        "#800000",  # Maroon
        "#00CED1",  # Dark Turquoise
        "#B22222",  # Firebrick
        "#FF4500",  # Orange Red
        "#1E90FF",  # Dodger Blue
        "#9400D3",  # Dark Violet
        "#00BFFF",  # Deep Sky Blue
        "#FF1493",  # Deep Pink
        "#20B2AA",  # Light Sea Green
        "#DC143C",  # Crimson
        "#7B68EE",  # Medium Slate Blue
        "#A0522D",  # Sienna
        "#1E90FF",  # Dodger Blue
        "#2E8B57",  # Sea Green
        "#FFD700",  # Gold
        "#191970",  # Midnight Blue
        "#F08080",  # Light Coral
        "#00FF00",  # Lime
        "#FF00FF",  # Magenta
        "#4169E1",  # Royal Blue
        "#808000",  # Olive
        "#FFFFE0",  # Light Yellow
        "#DA70D6",  # Orchid
        "#696969",  # Dim Gray
        "#FA8072",  # Salmon
        "#CD5C5C",  # Indian Red
        "#00FA9A",  # Medium Spring Green
        "#FAEBD7",  # Antique White
        "#32CD32",  # Lime Green
        "#87CEEB",  # Sky Blue
        "#8B008B",  # Dark Magenta
        "#ADFF2F",  # Green Yellow
        "#FFA07A",  # Light Salmon
        "#D2B48C",  # Tan
        "#8FBC8F",  # Dark Sea Green
    ]
    return random.choice(colors)
