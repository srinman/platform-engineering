# Contributing to Platform Engineering on AKS

Thank you for your interest in contributing! This document provides guidelines for contributing to this repository.

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Provide detailed information about the issue
- Include reproduction steps for bugs
- Tag appropriately (bug, enhancement, documentation, etc.)

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Guidelines

### Code Style

- **Terraform**: Follow [HashiCorp style guide](https://www.terraform.io/docs/language/syntax/style.html)
- **YAML**: Use 2-space indentation
- **Markdown**: Follow standard markdown formatting

### Testing

Before submitting:

1. **Terraform**: Run `terraform fmt` and `terraform validate`
2. **Kubernetes**: Validate YAML with `kubectl apply --dry-run=client`
3. **KRO**: Test ResourceGroups in a dev cluster

### Documentation

- Update README files when adding features
- Add comments to complex code
- Include examples for new scenarios
- Update GETTING-STARTED.md if workflow changes

## Adding a New Scenario

To add a new scenario:

1. Create directory structure:
```
scenarios/scenarioN/
├── README.md
├── kro-definitions/
│   └── resource-resourcegroup.yaml
├── examples/
│   └── example.yaml
└── monitoring/
    └── dashboards/
```

2. Document the scenario:
   - Problem statement
   - Solution overview
   - Architecture diagram
   - Quick start guide
   - DSL reference
   - Examples

3. Create KRO ResourceGroup
4. Provide working examples
5. Add monitoring/observability
6. Update main README.md

## Adding a Baseline Cluster

To add a new baseline cluster:

1. Create directory:
```
baseline-clusters/baseline-clusterN/
├── README.md
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars.example
└── gitops/
    └── bootstrap/
```

2. Document:
   - Purpose and use case
   - Features
   - Configuration options
   - Deployment steps

3. Test deployment end-to-end
4. Update main README.md

## Review Process

All contributions go through:

1. **Automated Checks**: Linting, validation
2. **Code Review**: Maintainer review
3. **Testing**: Deploy and verify
4. **Documentation Review**: Ensure docs are clear

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others in discussions
- Share knowledge and experiences

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open a GitHub Discussion
- Tag maintainers in issues
- Check existing documentation

Thank you for contributing! 🎉
