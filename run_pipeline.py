"""
GeoRiskAI Master Pipeline
Runs the full intelligence workflow.
"""

import os


print("\n🌍 Starting GeoRiskAI Pipeline...\n")


# =====================================================
# STEP 1 — LIVE NEWS
# =====================================================

print("STEP 1 — Running News Intelligence Engine...\n")

os.system(
    "python src/intelligence/news_engine.py"
)


# =====================================================
# STEP 2 — FUSION ENGINE
# =====================================================

print("\nSTEP 2 — Running Fusion Engine...\n")

os.system(
    "python src/intelligence/fusion_engine.py"
)


# =====================================================
# STEP 3 — INVESTOR ENGINE
# =====================================================

print("\nSTEP 3 — Running Investor Intelligence...\n")

os.system(
    "python src/intelligence/investor_engine.py"
)


# =====================================================
# STEP 4 — AI ANALYST
# =====================================================

print("\nSTEP 4 — Running AI Analyst...\n")

os.system(
    "python src/intelligence/ai_analyst.py"
)


# =====================================================
# COMPLETE
# =====================================================

print("\n✅ GeoRiskAI Pipeline Completed Successfully.\n")