# Quality gate: tests first, SonarQube last (owner rule 2026-10-21).
.PHONY: check test secrets sonar

check: test secrets sonar

test:
	./scripts/render_mermaid.sh
	python3 scripts/check_docs.py

secrets:
	gitleaks git --log-opts="main..HEAD" --no-banner
	@test -z "$$(git ls-files '.env*')" || { echo "tracked .env file"; exit 1; }

sonar:
	@test -n "$$SONAR_TOKEN" || { echo "SONAR_TOKEN is not set"; exit 1; }
	sonar-scanner -Dsonar.qualitygate.wait=true
