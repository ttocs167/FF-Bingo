
import requests
import time


def analyse_tea_fight(log_id, api_key):
    results = analyze_ultimate_fight(log_id, api_key, 1050)

    if results is None:
        return None

    best_fight = results["best_fight"]
    best_fight_time = time.strftime('%M:%S', time.gmtime(best_fight["length"]))
    active_time = time.strftime('%H:%M:%S', time.gmtime(results["active_time"]))
    total = results["total"]

    def phase_format(phase_id):
        phase_count = results[f"phase{phase_id}"]
        if phase_count == 0:
            return phase_count
        return f"{phase_count} ({phase_count/total*100:.1f}%)"

    message = f"""```
Total:   {total}
Living Liquid: {phase_format(1)}
Brute Justice: {phase_format(2)}
Alexander Prime: {phase_format(3)}
Phase 4: {phase_format(4)}
Active time: {active_time}
Embolus wipes: {results["embolus_wipes"]}

Best #{best_fight["id"]} {best_fight_time} (higher % the better)
Fight prog: {best_fight["fightPercentage"]:.2f}%
Phase prog: {best_fight["currentPhaseProg"]:.2f}%

Deaths:"""
    death_counts = results["death_counts"]
    for death_key in death_counts:
        message = message + f"\n{death_key}: {death_counts[death_key]}"
    return message + "```"


def analyse_uwu_fight(log_id, api_key):
    results = analyze_ultimate_fight(log_id, api_key, 1048)

    if results is None:
        return None

    best_fight = results["best_fight"]
    best_fight_time = time.strftime('%M:%S', time.gmtime(best_fight["length"]))
    active_time = time.strftime('%H:%M:%S', time.gmtime(results["active_time"]))
    total = results["total"]

    def phase_format(phase_id):
        phase_count = results[f"phase{phase_id}"]
        if phase_count == 0:
            return phase_count
        return f"{phase_count} ({phase_count/total*100:.1f}%)"

    message = f"""```
Total:   {total}
Garuda: {phase_format(1)}
Ifrit: {phase_format(2)}
Titan: {phase_format(3)}
Limit break: {phase_format(4)}
Ultima: {phase_format(5)}
Active time: {active_time}
Gaol wipes: {results.get("gaol_wipes", 0)}

Best #{best_fight["id"]} {best_fight_time} (higher % the better)
Fight prog: {best_fight["fightPercentage"]:.2f}%
Phase prog: {best_fight["currentPhaseProg"]:.2f}%

Deaths:"""
    death_counts = results["death_counts"]
    for death_key in death_counts:
        message = message + f"\n{death_key}: {death_counts[death_key]}"
    return message + "```"


def analyze_ultimate_fight(log_id, api_key, ultimate_id):
    response = requests.get(f"https://www.fflogs.com:443/v1/report/fights/{log_id}?api_key={api_key}")

    if response.status_code != 200:
        return None

    ultimate_fights = [fight for fight in response.json()['fights'] if fight['boss'] == ultimate_id]

    if len(ultimate_fights) == 0:
        return None

    last_fight = ultimate_fights[-1]
    death_reponse = requests.get(f"https://www.fflogs.com:443/v1/report/events/deaths/"
                                 f"{log_id}?end={last_fight['end_time']}&api_key={api_key}")

    deaths = None if death_reponse.status_code != 200 else death_reponse.json()['events']

    def get_deaths():
        if deaths is None:
            return None
        party_member_deaths = [death for death in deaths if death['targetIsFriendly'] is True]

        death_counts = {}
        for death in party_member_deaths:
            killing_ability = death.get('killingAbility')
            killing_ability_name = "Suicide" if killing_ability is None else death['killingAbility']['name']
            if death_counts.get(killing_ability_name) is not None:
                death_counts[killing_ability_name] = death_counts[killing_ability_name] + 1
            else:
                death_counts[killing_ability_name] = 1

        return death_counts

    fight_id = 1
    active_time = 0

    for fight in ultimate_fights:
        fight["id"] = fight_id
        fight_id = fight_id + 1

        active_time = active_time + fight["end_time"]/1000 - fight["start_time"]/1000

    def get_phase_count(phase):
        return len([fight for fight in ultimate_fights if fight['lastPhaseForPercentageDisplay'] == phase])
    best_fight = min(ultimate_fights, key=lambda f: f['fightPercentage'])
    results = {
        "total": len(ultimate_fights),
        "phase1": get_phase_count(1),
        "phase2": get_phase_count(2),
        "phase3": get_phase_count(3),
        "phase4": get_phase_count(4),
        "phase5": get_phase_count(5),
        "active_time": active_time,
        "best_fight": {
            "id": best_fight["id"],
            "length": (best_fight["end_time"] - best_fight["start_time"])/1000,
            "fightPercentage": 100 - best_fight['fightPercentage']/100,
            "currentPhaseProg": 100 - best_fight['bossPercentage']/100
        },
        "death_counts": get_deaths()
    }

    if ultimate_id == 1050:
        embolus = [enemy for enemy in response.json()['enemies'] if enemy['name'] == "Embolus"]
        embolus_wipes = len(embolus[0]['fights']) if len(embolus) == 1 else 0
        results["embolus_wipes"] = embolus_wipes

    if (ultimate_id == 1048) and (deaths is not None):
        gaol_deaths = [death for death in deaths if death.get('killingAbility') is not None
                       and (death['killingAbility']['name'] == 'Granite Impact')]
        gaol_death_fights = {}
        for gaol_death in gaol_deaths:
            gaol_death_fights[gaol_death["fight"]] = True
        results["gaol_wipes"] = len(gaol_death_fights)

    return results
