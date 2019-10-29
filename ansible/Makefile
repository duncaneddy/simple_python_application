# These secret files should also be added to .gitignore
SECRET_FILES=\
	host_vars/bethpage/secrets.yaml\
	host_vars/oceanside/secrets.yaml

.PHONY: help
help: ;

.PHONY: encrypt
encrypt:
	$(foreach file, $(SECRET_FILES), sops --encrypt $(file) > $(dir $(file)).sops.$(notdir $(file));)

.PHONY: decrypt
decrypt:
	$(foreach file, $(SECRET_FILES), sops --decrypt $(dir $(file)).sops.$(notdir $(file)) > $(file);)
