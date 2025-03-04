# Changelog

## [Unreleased] - 2023-07-02

### Added
- **API Testing Tools**:
  - Created `test_api.py`: A Python script for comprehensive API testing with detailed error handling
  - Created `test-api.sh`: A Bash script alternative for basic API testing
  - Generated `test-results/` directory with JSON responses for all endpoints
  - Made testing scripts executable with proper permissions

- **Documentation**:
  - Updated README.md with complete API documentation
  - Added detailed endpoint information with URL paths
  - Included sample request/response data for all endpoints
  - Added error handling examples with correct response formats
  - Added testing instructions for both Python and Bash scripts
  - Documented test results directory and its contents

### Changed
- **Security Enhancements**:
  - Enhanced authentication middleware to redact sensitive information in logs
  - Implemented sanitization for headers containing sensitive data
  - Specifically redacted `x-api-key`, `authorization`, `cookie`, and `x-auth-token` headers
  - Improved logging to only show detailed information in development environment

- **Documentation Updates**:
  - Updated Firestore data structure documentation to match actual implementation
  - Corrected error response examples based on actual API behavior
  - Improved formatting and organization of README.md

### Fixed
- Security issue with API key validation in logs
- Inconsistencies between documentation and actual API responses
- Dependencies in Python testing script to eliminate external requirements

### Technical Details
- The authentication middleware now creates a sanitized copy of headers before logging
- Testing scripts verify all endpoints and save responses to JSON files
- Python script uses ANSI color codes for better readability in terminal output
- All test results are saved in a structured format for documentation purposes 