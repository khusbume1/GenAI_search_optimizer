# Security Policy

## Supported version

The latest version on the default branch receives security fixes.

## Reporting

Do not open a public issue for a vulnerability involving credentials, command execution, path traversal, or access to non-public network resources. Contact the repository owner privately through the security reporting mechanism configured on GitHub.

## Operational guidance

- Keep Claude Code permissions restrictive.
- Do not place secrets in `GEO_CLAUDE_EXTRA_ARGS`.
- Audit only authorized public sites.
- Use network-level egress controls in production.
- Treat generated content and schema as untrusted until reviewed.
