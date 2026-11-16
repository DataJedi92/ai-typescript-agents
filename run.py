import argparse
from crew import build_crew, load_config

parser = argparse.ArgumentParser(description="Lancer le crew d'agents")
parser.add_argument("objective", nargs="?", default=(
    "Ajouter un écran de réglages avec un toggle thème sombre/clair persisté en AsyncStorage"))
parser.add_argument("--skip", nargs="*", default=[], help="ids à désactiver pour ce run")
parser.add_argument("--only", nargs="*", default=[], help="exécuter uniquement ces ids")
parser.add_argument("--enable", nargs="*", default=[], help="activer des ids désactivés dans le YAML")
parser.add_argument("--list", action="store_true", help="lister les agents et sortir")
args = parser.parse_args()

if args.list:
    for a in load_config()["agents"]:
        print(f"  {a['id']:12} {'✅ actif' if a.get('enabled', True) else '⛔ désactivé (YAML)'}  — {a['role']}")
    raise SystemExit

crew = build_crew(args.objective, skip=set(args.skip), only=set(args.only), enable=set(args.enable))
result = crew.kickoff()

print("\n" + "=" * 60)
print("RÉSULTAT FINAL")
print("=" * 60)
print(result.raw)

with open("agents/output.md", "w") as f:
    f.write(result.raw)