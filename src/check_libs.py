#!/usr/bin/env python3
"""
Check all required libraries for the Arabic AI Text Detection project
"""

libs = {
    # Core
    "pyspark":          "Apache Spark",
    "camel_tools":      "Arabic NLP (Camel-tools)",
    "nltk":             "Natural Language Toolkit",
    "numpy":            "NumPy",
    "matplotlib":       "Matplotlib (Visualization)",
    # Optional but useful
    "sklearn":          "Scikit-learn",
    "pandas":           "Pandas",
    "huggingface_hub":  "Hugging Face Hub",
}

print("=" * 50)
print(" Library Check — Arabic AI Detection Project")
print("=" * 50)

all_ok = True
for lib, name in libs.items():
    try:
        mod = __import__(lib)
        version = getattr(mod, "__version__", "installed")
        print(f"  ✅  {name:<30} {version}")
    except ImportError:
        print(f"  ❌  {name:<30} NOT INSTALLED")
        all_ok = False

print("=" * 50)

# Check Camel-tools database
try:
    from camel_tools.morphology.database import MorphologyDB
    from camel_tools.morphology.analyzer import Analyzer
    db = MorphologyDB.builtin_db()
    analyzer = Analyzer(db)
    result = analyzer.analyze('\u0643\u062a\u0628')
    print("  ✅  Camel-tools DB                 Ready")
except Exception as e:
    print(f"  ❌  Camel-tools DB                 {e}")
    all_ok = False

# Check Spark
try:
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("test").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    print(f"  ✅  Spark Session                  Ready")
    spark.stop()
except Exception as e:
    print(f"  ❌  Spark Session                  {e}")
    all_ok = False

print("=" * 50)
if all_ok:
    print("  🎉  All libraries are ready!")
else:
    print("  ⚠️   Some libraries are missing!")
print("=" * 50)
