from pathlib import PurePosixPath

from django.db import migrations


def move_menu_images_to_static(apps, schema_editor):
    MenuItem = apps.get_model("booking", "MenuItem")
    database = schema_editor.connection.alias

    for item in MenuItem.objects.using(database).exclude(uploaded_image="").iterator():
        filename = PurePosixPath(item.uploaded_image.name).name
        item.image_path = f"images/menu/{filename}"
        item.uploaded_image = ""
        item.save(update_fields=["image_path", "uploaded_image"])


def restore_menu_image_fields(apps, schema_editor):
    MenuItem = apps.get_model("booking", "MenuItem")
    database = schema_editor.connection.alias

    for item in MenuItem.objects.using(database).filter(image_path__startswith="images/menu/").iterator():
        filename = PurePosixPath(item.image_path).name
        item.uploaded_image = f"menu/{filename}"
        item.image_path = ""
        item.save(update_fields=["image_path", "uploaded_image"])


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0004_menuitem_uploaded_image_alter_menuitem_image_path"),
    ]

    operations = [
        migrations.RunPython(move_menu_images_to_static, restore_menu_image_fields),
    ]
