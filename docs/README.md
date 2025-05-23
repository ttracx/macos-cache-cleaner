# macOS Cache Cleaner Documentation

Welcome to the comprehensive documentation for the macOS Cache Cleaner project. This documentation covers everything from basic usage to advanced development topics.

## 📚 Documentation Index

### For Users

#### [User Guide](USER_GUIDE.md)
Complete guide for using the cache cleaner effectively:
- Getting started with different interfaces
- Understanding the desktop application
- Command-line usage and options
- Cleaning strategies for different use cases
- AI assistant features
- Best practices and FAQ

#### [Safety Guide](SAFETY_GUIDE.md)
Essential reading for understanding what's safe to clean:
- Built-in safety mechanisms
- Protected directories explained
- Risk levels for different cache types
- Recovery procedures if something goes wrong
- What never to clean manually

### For Developers

#### [Developer Guide](DEVELOPER_GUIDE.md)
Technical documentation for contributors and developers:
- Architecture overview
- Development environment setup
- Core components explained
- Building and testing procedures
- Contributing guidelines
- Creating plugins

#### [API Reference](API_REFERENCE.md)
Complete API documentation:
- Command-line interface
- Python API for scripting
- Electron/JavaScript APIs
- IPC communication protocols
- Plugin development API

#### [AI Integration](AI_INTEGRATION.md)
Deep dive into the AI assistant features:
- Architecture and setup
- Available AI features
- Customization options
- API reference for AI functions
- Troubleshooting guide

## 🚀 Quick Links

### Getting Started
- **New Users**: Start with the [User Guide](USER_GUIDE.md#getting-started)
- **Safety First**: Read the [Safety Guide](SAFETY_GUIDE.md#safety-overview)
- **Developers**: See [Development Setup](DEVELOPER_GUIDE.md#development-setup)

### Common Tasks
- [Using the Desktop App](USER_GUIDE.md#desktop-application)
- [Command Line Options](API_REFERENCE.md#command-line-interface)
- [Setting Up AI Assistant](AI_INTEGRATION.md#setup-guide)
- [Understanding Cache Types](SAFETY_GUIDE.md#cache-types-explained)

### Troubleshooting
- [Common Issues](USER_GUIDE.md#troubleshooting)
- [AI Problems](AI_INTEGRATION.md#troubleshooting)
- [Recovery Procedures](SAFETY_GUIDE.md#recovery-procedures)

## 📊 Quick Reference

### Cleaning Modes

| Mode | Safety | Speed | Space Freed | Use Case |
|------|--------|-------|-------------|----------|
| Scan Only | ✅✅✅ | Fast | 0 GB | Preview |
| Safe Clean | ✅✅ | Medium | 1-5 GB | Regular |
| Deep Clean | ✅ | Slow | 5-20 GB | Quarterly |

### Risk Levels

- 🟢 **Low Risk**: Browser caches, npm caches, old logs
- 🟡 **Medium Risk**: Docker caches, development builds
- 🔴 **High Risk**: Application data, preferences, keychains

### Command Cheat Sheet

```bash
# Preview what will be cleaned
./cache_cleaner.py --dry-run --verbose

# Safe cleanup
./cache_cleaner.py --skip-trash --skip-maintenance

# Deep clean with all features
sudo ./cache_cleaner.py --find-large-files

# Launch desktop app
cd electron-app && ./run.sh
```

## 🤝 Contributing to Documentation

Found an error or want to improve the documentation?

1. Fork the repository
2. Edit the relevant `.md` file in the `docs/` directory
3. Submit a pull request

### Documentation Style Guide

- Use clear, concise language
- Include code examples where relevant
- Add screenshots for UI features
- Keep formatting consistent
- Update the table of contents when adding sections

## 📈 Version History

| Version | Documentation Updates |
|---------|---------------------|
| 2.0.0 | Added AI integration docs, Electron app guide |
| 1.0.0 | Initial documentation release |

## 🔗 External Resources

- [Project Repository](https://github.com/ttracx/macos-cache-cleaner)
- [Issue Tracker](https://github.com/ttracx/macos-cache-cleaner/issues)
- [Ollama Documentation](https://ollama.ai/docs) (for AI features)
- [Electron Documentation](https://www.electronjs.org/docs) (for desktop app)

## 📧 Support

For documentation-related questions:
- Check the relevant guide first
- Search existing GitHub issues
- Create a new issue with the `documentation` label
- Contact: mail@tommytracx.com

---

**Note**: This documentation is for macOS Cache Cleaner v2.0.0. Always check you're reading the documentation version that matches your installed version.