import json
from typing import Any

from db.models import Race, Skill, Guild, Player


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if not line.strip():
            continue

        player_data: dict[str, Any] = json.loads(line)

        # --- RACE ---
        race_info = player_data["race"]
        race, _ = Race.objects.get_or_create(
            name=race_info["name"],
            defaults={"description": race_info.get("description", "")}
        )

        # --- SKILLS ---
        for skill_info in race_info.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_info["name"],
                defaults={
                    "bonus": skill_info["bonus"],
                    "race": race
                }
            )

        # --- GUILD ---
        guild_obj = None
        guild_info = player_data.get("guild")

        if guild_info is not None:
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_info["name"],
                defaults={"description": guild_info.get("description")}
            )

        # --- PLAYER ---
        Player.objects.get_or_create(
            nickname=player_data["nickname"],
            defaults={
                "email": player_data["email"],
                "bio": player_data["bio"],
                "race": race,
                "guild": guild_obj,
            }
        )
