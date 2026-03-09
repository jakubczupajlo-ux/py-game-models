import json
from typing import Any

from db.models import Race, Skill, Guild, Player


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as file:
        players_data: list[dict[str, Any]] = json.load(file)

    for player in players_data:
        # --- RACE ---
        race_data = player["race"]
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data.get("description", "")}
        )

        # --- SKILLS ---
        skills_data = race_data.get("skills", [])
        for skill in skills_data:
            Skill.objects.get_or_create(
                name=skill["name"],
                defaults={
                    "bonus": skill["bonus"],
                    "race": race
                }
            )

        # --- GUILD ---
        guild_obj = None
        guild_data = player.get("guild")

        if guild_data is not None:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")}
            )

        # --- PLAYER ---
        Player.objects.get_or_create(
            nickname=player["nickname"],
            defaults={
                "email": player["email"],
                "bio": player["bio"],
                "race": race,
                "guild": guild_obj,
            }
        )


if __name__ == "__main__":
    main()
