import json
from django.utils import timezone

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as config_file:
        data = json.load(config_file)

    for value in data.values():
        race, created = Race.objects.get_or_create(
            name=value["race"]["name"],
            defaults={
                "description": value["race"].get("description", ""),
            }
        )
        for skill in value["race"]["skills"]:
            Skill.objects.get_or_create(
                name=skill["name"],
                defaults={
                    "bonus": skill["bonus"],
                    "race": race
                }
            )
    for player in data.values():
        if player["guild"]:
            Guild.objects.get_or_create(
                name=player["guild"]["name"],
                defaults={
                    "description": player["guild"].get("description", ""),
                }
            )

    for key, value in data.items():
        race = Race.objects.get(name=value["race"]["name"])
        guild_name = value["guild"]["name"] if value["guild"] else None
        guild = Guild.objects.filter(name=guild_name).first()

        Player.objects.get_or_create(
            nickname=key,
            defaults={
                "email": value["email"],
                "bio": value["bio"],
                "race": race,
                "guild": guild,
                "created_at": timezone.now(),
            }
        )


if __name__ == "__main__":
    main()
