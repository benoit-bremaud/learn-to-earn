# Quality gate: every test first, SonarQube last (owner rule 2026-10-21).
# Prerequisites: python3, gitleaks >= 8.19, mmdc + Chrome, sonar-scanner, SONAR_TOKEN.
PY := .venv/bin/python

.PHONY: check ci venv test secrets sonar

check: test secrets sonar

# GitHub Actions: everything but SonarQube (the instance is local).
ci: test secrets

venv:
	python3 -m venv .venv && .venv/bin/pip install -q -r requirements-dev.txt

test:
	@test -x $(PY) || { echo "run make venv first"; exit 1; }
	$(PY) -m coverage run --branch --source=scripts --omit='scripts/test_*' -m unittest discover -s scripts -v
	$(PY) -m coverage xml -o coverage.xml
	$(PY) -m coverage report --fail-under=80
	./scripts/render_mermaid.sh
	$(PY) scripts/check_docs.py

secrets:
	gitleaks git --no-banner
	gitleaks dir . --no-banner
	@test -z "$$(git ls-files '.env*' | grep -v '\.env\.example$$')" || { echo "tracked .env file"; exit 1; }

sonar:
	@test -n "$$SONAR_TOKEN" || { echo "SONAR_TOKEN is not set"; exit 1; }
	sonar-scanner -Dsonar.qualitygate.wait=true
