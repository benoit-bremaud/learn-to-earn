# learn-to-earn (working title)

A mobile and web app that helps a CE1 child (7–8 years old) master arithmetic, aligned with the French national curriculum. The app adapts to the child (correctness and response speed), insists on weak skills, and turns good work into earned screen time. The better you work, the more you may watch or play.

Status: design phase. The project brief is in [docs/CADRAGE.md](docs/CADRAGE.md) and the curriculum mapping in [docs/curriculum/CE1-maths.md](docs/curriculum/CE1-maths.md). The name is provisional.

Quality: `make check` runs every test, the secrets scan, then the SonarQube gate on the local instance. GitHub Actions runs the same checks without SonarQube (`make ci`).

Privacy by design: local-first storage, no trackers, no child data sent to third parties. No licence has been chosen yet, so all rights are reserved by default until it is.
