# Quality gate: tests first, SonarQube last (owner rule 2026-10-21).
.PHONY: check test secrets sonar venv

venv:
	python3 -m venv .venv && .venv/bin/pip install -q -r requirements-dev.txt

check: test secrets sonar

PY := .venv/bin/python

test:
	$(PY) -m coverage run --source=scripts -m unittest discover -s scripts -v
	$(PY) -m coverage xml -o coverage.xml
	$(PY) -m coverage report --fail-under=80
	./scripts/render_mermaid.sh
	$(PY) scripts/check_docs.py

secrets:
	gitleaks git --log-opts="main..HEAD" --no-banner
	@test -z "$$(git ls-files '.env*')" || { echo "tracked .env file"; exit 1; }

sonar:
	@test -n "$$SONAR_TOKEN" || { echo "SONAR_TOKEN is not set"; exit 1; }
	sonar-scanner -Dsonar.qualitygate.wait=true
