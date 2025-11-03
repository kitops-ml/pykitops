.PHONY: version-bump

version-bump:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION parameter is required. Usage: make version-bump VERSION=1.4.0"; \
		exit 1; \
	fi
	sed -i '' 's/^__version__ = ".*"$$/__version__ = "$(VERSION)"/' kitops/__init__.py
	sed -i '' 's/^version = ".*"$$/version = "$(VERSION)"/' pyproject.toml
	@echo "Version bumped to $(VERSION)"
