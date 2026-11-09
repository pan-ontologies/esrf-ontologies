"""Validate the ontologies with ROBOT (https://robot.obolibrary.org/).

Requires Java and either the `robot` command or the ROBOT jar file:

    python ontologies/check_robot.py --robot-jar robot.jar
"""

import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from typing import List
from typing import Optional

ONTOLOGIES_DIR = Path(__file__).parent

ONTOLOGY_FILES = [
    "esrfet/ESRFET.owl",
    "esrffair/ESRFFAIR.owl",
]

ROBOT_DIR = ONTOLOGIES_DIR / "robot"

# Resolve imports (e.g. PaNET) to local files instead of downloading them.
CATALOG = ROBOT_DIR / "catalog.xml"

# Report rules adapted to our conventions (skos:prefLabel, rdfs:comment, ...).
# Custom rules in the profile are relative to ROBOT_DIR.
REPORT_PROFILE = ROBOT_DIR / "profile.txt"


def run_robot(
    robot: List[str], args: List[str], log_file: Optional[Path] = None
) -> bool:
    cmd = robot + ["--catalog", str(CATALOG)] + args
    print(f"$ {shlex.join(cmd)}", flush=True)
    # Run from ROBOT_DIR so relative custom rules in the profile are found.
    result = subprocess.run(  # noqa: S603 (fixed command)
        cmd,
        cwd=ROBOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(result.stdout, end="", flush=True)
    if log_file is not None:
        log_file.write_text(result.stdout)
    return result.returncode == 0


def check_ontology(robot: List[str], owl_file: str, report_dir: Path) -> List[str]:
    owl_path = str(ONTOLOGIES_DIR / owl_file)
    name = Path(owl_file).stem
    errors = []

    # Ontology and its imports must be in the OWL 2 DL profile.
    if not run_robot(
        robot,
        [
            "validate-profile",
            "--input",
            owl_path,
            "--profile",
            "DL",
            "--output",
            str(report_dir / f"{name}_profile.txt"),
        ],
    ):
        errors.append(f"{owl_file}: not in the OWL 2 DL profile")

    # Ontology must be consistent, without unsatisfiable classes
    # and without inferred (not asserted) equivalent classes.
    if not run_robot(
        robot,
        [
            "reason",
            "--input",
            owl_path,
            "--reasoner",
            "HermiT",
            "--equivalent-classes-allowed",
            "asserted-only",
        ],
        log_file=report_dir / f"{name}_reason.txt",
    ):
        errors.append(
            f"{owl_file}: inconsistent, unsatisfiable classes "
            "or inferred equivalent classes"
        )

    # Quality report for information only: HTML to read, TSV to process.
    for extension in ("html", "tsv"):
        run_robot(
            robot,
            [
                "report",
                "--input",
                owl_path,
                "--profile",
                str(REPORT_PROFILE),
                "--fail-on",
                "none",
                "--output",
                str(report_dir / f"{name}_report.{extension}"),
            ],
        )

    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--robot-jar",
        help="Path to the ROBOT jar file (default: use the 'robot' command)",
    )
    parser.add_argument(
        "--report-dir",
        default=str(ONTOLOGIES_DIR.parent / "build" / "robot"),
        help="Directory for the ROBOT profile and quality reports",
    )
    args = parser.parse_args(argv)

    if args.robot_jar:
        robot = ["java", "-jar", str(Path(args.robot_jar).resolve())]
    else:
        robot = ["robot"]
    report_dir = Path(args.report_dir).resolve()
    report_dir.mkdir(parents=True, exist_ok=True)

    all_errors = []
    for owl_file in ONTOLOGY_FILES:
        errors = check_ontology(robot, owl_file, report_dir)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"Checked: {owl_file}: OK")

    print(f"Reports: {report_dir}")
    for error in all_errors:
        print(f"Error: {error}")

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
