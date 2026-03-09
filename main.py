import json
import init_django_orm

from db.models import Race, Skill, Guild, Player


def main() -> None:
    with open("players.json", "r") as file:
        players_data = json.load(file)

    for nickname, data in players_data.items():
        # Pobieranie rasy
        race_info = data.get("race")
        race, _ = Race.objects.get_or_create(
            name=race_info.get("name"),
            defaults={"description": race_info.get("description")}
        )

        # Pobieranie skilli dla tej rasy
        for skill_info in race_info.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_info.get("name"),
                race=race,
                defaults={"bonus": skill_info.get("bonus")}
            )

        # Pobieranie gildii (jeśli istnieje)
        guild_info = data.get("guild")
        guild = None
        if guild_info:
            guild, _ = Guild.objects.get_or_create(
                name=guild_info.get("name"),
                defaults={"description": guild_info.get("description")}
            )

        # Tworzenie gracza
        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": data.get("email"),
                "bio": data.get("bio"),
                "race": race,
                "guild": guild
            }
        )


if __name__ == "__main__":
    main()
