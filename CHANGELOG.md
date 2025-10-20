# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Professional GitHub README with bilingual support
- AI summary feature for long highlights
- AI smart tags with topic extraction
- Cookie Cloud support for auto-syncing browser cookies
- Test script for single highlight sync
- Comprehensive documentation in `docs/` directory
- GitHub Actions workflow for automated sync
- Issue templates for bugs and feature requests
- Contributing guidelines
- English README (README_EN.md)
- 🎉 Automatic failure notification via Issue creation
- 📊 GitHub Actions Summary for sync statistics
- 📝 Complete log file preservation (30 days retention)
- 🕐 Localized time display (Asia/Shanghai timezone)
- ⏰ Flexible cron schedule options with examples
- 🔍 Detailed error analysis in auto-created Issues

### Changed
- Enhanced template system with AI summary section
- Improved configuration management
- Better error handling and logging
- Optimized sync performance
- 🔧 Smart environment variable handling (only write non-empty values)
- 🔧 Enhanced Secrets priority: manual input > Secrets > config defaults

### Fixed
- Cookie refresh mechanism
- Bookmark list API handling
- Chapter info retrieval timing
- 🐛 Environment variable type safety (empty string handling)
- 🐛 TypeError when comparing string with int in config manager

## [1.0.0] - 2024-10-17

### Added
- Core sync functionality
- Multi-template system (Simple/Standard/Detailed)
- AI tag generation
- Book categorization
- Time-based filtering
- Incremental sync with deduplication
- Flexible configuration system
- GitHub Actions support

### Features
- 📝 Auto-sync WeRead highlights to Flomo
- 🎨 Multiple templates for different use cases
- 🤖 AI-powered tag generation
- 📚 Smart book categorization
- ⏱️ Time-based filtering
- 🔄 Incremental sync
- ⚙️ Flexible configuration

---

## Version History

### Legend
- 🎉 Major feature
- ✨ Minor feature
- 🐛 Bug fix
- 📝 Documentation
- 🔧 Configuration
- ⚡ Performance
- 🔒 Security

---

## Future Releases

### [1.1.0] - Planned
- [ ] Web management interface
- [ ] Multi-account support
- [ ] Batch editing
- [ ] More template presets

### [1.2.0] - Planned
- [ ] Export to Markdown/PDF
- [ ] Notion integration
- [ ] Obsidian integration
- [ ] Mobile app support

### [2.0.0] - Planned
- [ ] Knowledge graph visualization
- [ ] Note linking and references
- [ ] AI conversational search
- [ ] Community template marketplace

---

For more information, see the [Roadmap](README.md#-路线图).

