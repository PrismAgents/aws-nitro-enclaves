# === CLEAN ===
.PHONY: clean
clean:
        ENCLAVE_ID=$$(nitro-cli describe-enclaves | jq -r ".[0].EnclaveID"); \
        if [ "$$ENCLAVE_ID" != "null" ]; then \
                echo "Stopping enclave $$ENCLAVE_ID..."; \
                nitro-cli terminate-enclave --enclave-id $$ENCLAVE_ID; \
        fi
