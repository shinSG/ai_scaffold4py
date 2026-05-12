import argparse
import re
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def to_package_name(project_name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9\-\s]", "", project_name.strip().lower())
    normalized = normalized.replace("-", "_").replace(" ", "_")
    normalized = re.sub(r"_+", "_", normalized)
    if not normalized or not normalized[0].isalpha():
        normalized = f"app_{normalized or 'project'}"
    return normalized


def render_project(project_name: str, target_dir: Path, force: bool, dry_run: bool) -> None:
    if target_dir.exists() and any(target_dir.iterdir()) and not force:
        raise SystemExit(f"Target directory is not empty: {target_dir}. Use --force to continue.")

    package_name = to_package_name(project_name)
    context = {
        "project_name": project_name,
        "package_name": package_name,
    }

    template_root = Path(__file__).parent / "templates" / "project"
    env = Environment(loader=FileSystemLoader(str(template_root)), autoescape=False)

    for template_file in template_root.rglob("*.j2"):
        relative = template_file.relative_to(template_root)
        output_relative = Path(str(relative).replace(".j2", ""))
        output_path = target_dir / output_relative

        if dry_run:
            print(f"[DRY-RUN] create {output_path}")
            continue

        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = env.get_template(str(relative).replace("\\", "/"))
        output_path.write_text(template.render(**context), encoding="utf-8")

    if not dry_run:
        print(f"Project generated at: {target_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a new agent scaffold project")
    parser.add_argument("--project-name", help="Project display name")
    parser.add_argument("--target-dir", default=".", help="Target directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Preview files only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_name = args.project_name or input("Please input project name: ").strip()
    if not project_name:
        raise SystemExit("Project name is required")

    target_dir = Path(args.target_dir).resolve()
    if args.force and target_dir.exists() and not args.dry_run:
        shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    render_project(project_name, target_dir, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
