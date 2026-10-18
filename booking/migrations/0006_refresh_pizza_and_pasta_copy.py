from django.db import migrations


MENU_COPY = {
    "purely-pizza": (
        "Rustic Tomato Pan Pizza",
        "rustic-tomato-pan-pizza",
        "Slow-baked on a thick, golden crust, this rustic pan pizza is layered with rich tomato sauce and baked until fragrant and crisp at the edges.",
    ),
    "pizza": (
        "Golden Tomato Pizza",
        "golden-tomato-pizza",
        "A simple oven-baked pizza with a crisp base and savory tomato topping—comforting, satisfying, and perfect for a quick bite.",
    ),
    "pasta": (
        "Basil-Kissed Penne",
        "basil-kissed-penne",
        "Tender penne finished with fresh basil leaves for a light, fragrant pasta that keeps every bite simple and satisfying.",
    ),
    "pique-pasta": (
        "Tomato & Basil Fusilli",
        "tomato-basil-fusilli",
        "Corkscrew fusilli coated in a bright tomato sauce, with basil and garlic bringing a fresh, savory finish.",
    ),
}


def update_menu_copy(apps, schema_editor):
    MenuItem = apps.get_model("booking", "MenuItem")
    database = schema_editor.connection.alias

    for old_slug, (name, slug, description) in MENU_COPY.items():
        MenuItem.objects.using(database).filter(slug=old_slug).update(
            name=name,
            slug=slug,
            description=description,
        )


def restore_menu_copy(apps, schema_editor):
    MenuItem = apps.get_model("booking", "MenuItem")
    database = schema_editor.connection.alias
    old_names = {
        "rustic-tomato-pan-pizza": ("purely pizza", "purely-pizza", "an amazing freshed pizza"),
        "golden-tomato-pizza": ("pizza", "pizza", "graet prepared"),
        "basil-kissed-penne": ("pasta", "pasta", "an amazing"),
        "tomato-basil-fusilli": ("pique pasta", "pique-pasta", "grattahb"),
    }

    for slug, (name, old_slug, description) in old_names.items():
        MenuItem.objects.using(database).filter(slug=slug).update(
            name=name,
            slug=old_slug,
            description=description,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0005_menu_images_to_static"),
    ]

    operations = [
        migrations.RunPython(update_menu_copy, restore_menu_copy),
    ]
