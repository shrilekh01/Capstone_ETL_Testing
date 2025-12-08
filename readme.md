# Pytest Commands Reference - Capstone ETL Testing

## Prerequisites
```bash
pip install pytest pytest-html pytest-xdist
```

---

## 1. Run ALL Tests
```bash
pytest -v -s
```

---

## 2. Run Tests by Marker

### Run SMOKE Tests Only (Critical Tests)
```bash
pytest -v -s -m smoke
```

### Run REGRESSION Tests Only (Complete Suite)
```bash
pytest -v -s -m regression
```

### Run DATA QUALITY Tests Only
```bash
pytest -v -s -m dq
```

### Run EXTRACTION Tests Only
```bash
pytest -v -s -m extraction
```

### Run TRANSFORMATION Tests Only
```bash
pytest -v -s -m transformation
```

### Run LOADING Tests Only
```bash
pytest -v -s -m loading
```

---

## 3. Run Specific Test Files

### Run Extraction Tests Only
```bash
pytest test_data_extraction.py -v -s
```

### Run Transformation Tests Only
```bash
pytest test_data_transformation.py -v -s
```

### Run Loading Tests Only
```bash
pytest test_data_loading.py -v -s
```

### Run Data Quality Tests Only
```bash
pytest test_data_quality.py -v -s
```

---

## 4. Run with HTML Reports

### Generate Single HTML Report
```bash
pytest -v -s --html=Reports/test_report.html --self-contained-html
```

### Generate Smoke Test Report
```bash
pytest -v -s -m smoke --html=Reports/SmokeTestResults.html --self-contained-html
```

### Generate Regression Test Report
```bash
pytest -v -s -m regression --html=Reports/RegressionTestResults.html --self-contained-html
```

### Generate Data Quality Test Report
```bash
pytest -v -s -m dq --html=Reports/DataQualityTestResults.html --self-contained-html
```

---

## 5. Run with Logging

### Log to File with INFO Level
```bash
pytest -v -s --log-file=Logs/test_execution.log --log-level=INFO
```

### Log to File with HTML Report
```bash
pytest -v -s -m smoke \
  --log-file=Logs/smoke_test.log \
  --log-level=INFO \
  --html=Reports/SmokeTestResults.html \
  --self-contained-html
```

---

## 6. Run Tests in Parallel (Faster Execution)

### Run with Auto Worker Count
```bash
pytest -v -s -n auto
```

### Run with Specific Worker Count
```bash
pytest -v -s -n 4
```

### Run Regression in Parallel with HTML Report
```bash
pytest -v -s -m regression -n auto --html=Reports/RegressionTestResults.html --self-contained-html
```

---

## 7. Run Specific Test Cases

### Run Single Test Case
```bash
pytest test_data_extraction.py::TestDataExtraction::test_DE_from_sales_data_between_source_and_staging -v -s
```

### Run Multiple Test Cases by Pattern
```bash
pytest -k "sales" -v -s
```

### Run Tests by Keyword Match
```bash
pytest -k "duplicate" -v -s
```

---

## 8. Combined Commands (Most Common)

### Complete Smoke Test with Report
```bash
pytest -v -s -m smoke \
  --log-file=Logs/smoke_test.log \
  --log-level=INFO \
  --html=Reports/SmokeTestResults.html \
  --self-contained-html
```

### Complete Regression Test with Report
```bash
pytest -v -s -m regression \
  --log-file=Logs/regression_test.log \
  --log-level=INFO \
  --html=Reports/RegressionTestResults.html \
  --self-contained-html
```

### Complete Data Quality Test with Report
```bash
pytest -v -s -m dq \
  --log-file=Logs/dq_test.log \
  --log-level=INFO \
  --html=Reports/DataQualityTestResults.html \
  --self-contained-html
```

### All Tests in Parallel with Report
```bash
pytest -v -s -n auto \
  --log-file=Logs/all_tests.log \
  --log-level=INFO \
  --html=Reports/AllTestResults.html \
  --self-contained-html
```

---

## 9. Useful Pytest Options

| Option | Description |
|--------|-------------|
| `-v` | Verbose output (show test names) |
| `-s` | Show print statements and logs in console |
| `-m marker` | Run tests with specific marker |
| `-k pattern` | Run tests matching pattern |
| `-x` | Stop on first failure |
| `--tb=short` | Short traceback format |
| `--tb=no` | No traceback |
| `-n auto` | Parallel execution (auto workers) |
| `--html=path` | Generate HTML report |
| `--self-contained-html` | Single file HTML report |
| `--log-file=path` | Log to file |
| `--log-level=LEVEL` | Set log level (DEBUG, INFO, WARNING, ERROR) |

---

## 10. Jenkins Integration Commands

### Smoke Test Suite (for Build Verification)
```bash
pytest -v -s -m smoke \
  --log-file=Logs/smoke_test.log \
  --log-level=INFO \
  --html=Reports/SmokeTestResults.html \
  --self-contained-html \
  --junitxml=Reports/smoke_junit.xml
```

### Regression Test Suite (for Complete Testing)
```bash
pytest -v -s -m regression -n auto \
  --log-file=Logs/regression_test.log \
  --log-level=INFO \
  --html=Reports/RegressionTestResults.html \
  --self-contained-html \
  --junitxml=Reports/regression_junit.xml
```

---

## Example Test Execution Flow

### 1. Quick Smoke Test (2-5 minutes)
```bash
pytest -v -s -m smoke
```

### 2. If Smoke Passes → Run Regression (10-15 minutes)
```bash
pytest -v -s -m regression -n auto
```

### 3. Generate Final Reports
```bash
pytest -v -s \
  --log-file=Logs/final_test.log \
  --log-level=INFO \
  --html=Reports/FinalTestResults.html \
  --self-contained-html
```