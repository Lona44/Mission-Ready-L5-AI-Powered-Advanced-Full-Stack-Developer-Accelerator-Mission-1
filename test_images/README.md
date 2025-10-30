# Test Images

Sample images used for out-of-distribution testing and validation.

## Contents

- `mission_01_task.png` - Original project task screenshot
- Various car images used for testing model predictions

## Purpose

These images are **not part of the training dataset**. They were used to:
- Test model performance on real-world images
- Validate API endpoints
- Identify edge cases and failure modes
- Create documentation examples

## Testing Results

See `docs/VALIDATION_TEST_RESULTS.md` for detailed test results.

## Note

Large test images are excluded from Git via `.gitignore` to keep the repository size small. The validation test set is available in `data/validation_test_set/` (also excluded from Git).
