"""
GeoRiskAI Auto Intelligence Pipeline
Automatically refreshes geopolitical intelligence.
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time


scheduler = BlockingScheduler()


# =====================================================
# MAIN PIPELINE
# =====================================================

def run_pipeline():

    print("\n🌍 Refreshing GeoRiskAI Intelligence...\n")

    # =============================================
    # NEWS ENGINE
    # =============================================

    print("Running News Engine...\n")

    os.system(
        "python src/intelligence/news_engine.py"
    )

    time.sleep(2)

    # =============================================
    # FUSION ENGINE
    # =============================================

    print("\nRunning Fusion Engine...\n")

    os.system(
        "python src/intelligence/fusion_engine.py"
    )

    time.sleep(2)

    # =============================================
    # INVESTOR ENGINE
    # =============================================

    print("\nRunning Investor Engine...\n")

    os.system(
        "python src/intelligence/investor_engine.py"
    )

    time.sleep(2)

    print("\n✅ GeoRiskAI Updated Successfully.\n")


# =====================================================
# SCHEDULE
# =====================================================

scheduler.add_job(
    run_pipeline,
    "interval",
    minutes=30
)


# =====================================================
# START
# =====================================================

print(
    "\n🚀 GeoRiskAI Auto Pipeline Started...\n"
)

print(
    "Updating every 30 minutes...\n"
)

run_pipeline()

scheduler.start()