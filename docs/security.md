# Security Architecture & Policies

## 1. Password Hashing (Argon2id)
The application strictly uses **Argon2id** (winner of the Password Hashing Competition) configured with modern cryptographic parameters:
- **Algorithm**: Argon2id (`v=19`)
- **Memory Cost**: 65,536 KiB (64 MiB)
- **Time Cost (Iterations)**: 3 passes
- **Parallelism**: 4 lanes
- **Salt Length**: 16 bytes random salt

Never use MD5, SHA-1, SHA-256, or vanilla bcrypt for user passwords.

---

## 2. Authentication & JWT Tokens
- **Access Tokens**: Short-lived (default: 30 minutes) carrying minimal claims (`sub`, `role`, `email`, `iat`, `exp`, `type`).
- **Refresh Tokens**: Long-lived (default: 30 days) with dedicated token type validation.
- **Algorithm**: `HS256` (or `RS256` / `EdDSA` when transitioning to asymmetric key rotation).

---

## 3. Secrets Management
- **Zero Hardcoded Secrets**: Secrets are NEVER hardcoded into source control or Docker images.
- **Environment Driven**: Secrets are provided via environment variables, `.env` files (excluded from git), or external vaults (Azure Key Vault / AWS Secrets Manager).
- **Safe Fallbacks**: Missing non-essential external secrets (e.g. OpenAI or Stripe API keys) will not crash basic application boot unless the corresponding feature path is invoked.

---

## 4. Automated Security Scanning
1. **Bandit**: Static application security testing (SAST) scanning for common Python vulnerabilities, dangerous functions, and weak cryptography.
2. **pip-audit**: Dependency vulnerability scanning checking installed packages against the Python Packaging Advisory Database (PyPA) and OSV.
3. **Automated CI Enforcement**: Both Bandit and pip-audit run on every push and pull request via `.github/workflows/ci.yml`.
