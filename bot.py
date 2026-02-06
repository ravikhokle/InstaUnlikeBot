print("🚀 BOT STARTED", flush=True)

import time
import random
import traceback
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from credentials import USERNAME, PASSWORD

# =========================================================
# ======================= CONFIG ==========================
# =========================================================

# -------- SPEED PROFILE --------
# "slow" | "safe" | "fast" | "aggressive"
SPEED_PROFILE = "fast"

# -------- LIMITS --------
BATCH_SIZE = 100           # unlikes per batch
MAX_BATCHES = 20           # batches per run
DAILY_MAX_UNLIKES = 5000    # hard stop safety

# -------- TIMING --------
WAIT_TIMEOUT = 30
SCROLL_STEP = 3000

LIKES_URL = "https://www.instagram.com/your_activity/interactions/likes/"

# =========================================================
# ================= SPEED CONTROLLER ======================
# =========================================================

SPEEDS = {
    "slow": {
        "click": (0.8, 1.5),
        "burst": (1.5, 2.5),
        "batch_pause": (40, 60),
        "scroll": 1.5,
    },
    "safe": {
        "click": (0.4, 0.8),
        "burst": (0.8, 1.2),
        "batch_pause": (25, 40),
        "scroll": 1.0,
    },
    "fast": {
        "click": (0.15, 0.35),
        "burst": (0.5, 0.8),
        "batch_pause": (10, 18),
        "scroll": 0.6,
    },
    "aggressive": {
        "click": (0.05, 0.15),
        "burst": (0.2, 0.4),
        "batch_pause": (4, 8),
        "scroll": 0.3,
    },
}

PROFILE = SPEEDS[SPEED_PROFILE]

# =========================================================
# ======================= HELPERS =========================
# =========================================================

def log(msg):
    print(f"[DEBUG] {msg}", flush=True)

def r_sleep(a, b):
    time.sleep(random.uniform(a, b))

def burst_sleep():
    time.sleep(random.uniform(*PROFILE["burst"]))

def click_sleep():
    time.sleep(random.uniform(*PROFILE["click"]))

def ensure_in_view(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
        element,
    )
    time.sleep(0.1)

# =========================================================
# ======================== BOT ============================
# =========================================================

try:
    # ---------- DRIVER ----------
    log("Launching Chrome")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # ---------- LOGIN ----------
    log("Opening login page")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(15)

    user_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    pass_input = wait.until(EC.presence_of_element_located((By.NAME, "pass")))

    user_input.send_keys(USERNAME)
    r_sleep(1, 2)
    pass_input.send_keys(PASSWORD)
    r_sleep(1, 2)

    login_btn = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//form[@id='login_form']//div[@role='button'][.//span[normalize-space()='Log in']]"
    )))
    driver.execute_script("arguments[0].click();", login_btn)

    r_sleep(15, 20)

    # ---------- GO TO LIKES ----------
    driver.get(LIKES_URL)
    r_sleep(6, 8)

    total_unliked = 0

    # ================= BATCH LOOP =================
    for batch_no in range(1, MAX_BATCHES + 1):
        if total_unliked >= DAILY_MAX_UNLIKES:
            log("🛑 Daily limit reached")
            break

        log(f"🚀 Starting batch {batch_no}")

        # ---------- SELECT ----------
        for _ in range(10):
            try:
                btn = driver.find_element(By.XPATH, "//span[text()='Select']")
                driver.execute_script("arguments[0].click();", btn)
                break
            except:
                time.sleep(1)
        else:
            log("❌ Select not found")
            break

        selected = 0
        seen = set()

        # ---------- FAST SELECTION ----------
        while selected < BATCH_SIZE:
            posts = driver.find_elements(
                By.XPATH,
                "//div[@role='button' and (" 
                "@aria-label='Image of Post' or "
                "contains(@aria-label, 'Reel') or "
                "contains(@aria-label, 'Video')"
                ")]",
            )

            if not posts:
                break

            for post in posts:
                if selected >= BATCH_SIZE:
                    break

                pid = post.get_attribute("outerHTML")
                if pid in seen:
                    continue
                seen.add(pid)

                ensure_in_view(driver, post)
                driver.execute_script("arguments[0].click();", post)
                selected += 1
                total_unliked += 1

                log(f"Selected {selected} | Total {total_unliked}")
                click_sleep()

                if selected % 3 == 0:
                    burst_sleep()

            if selected < BATCH_SIZE:
                driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")
                time.sleep(PROFILE["scroll"])

        if selected == 0:
            log("⚠️ Nothing selected")
            break

        # ---------- UNLIKE ----------
        unlike_btn = wait.until(EC.presence_of_element_located((
            By.XPATH, "//span[normalize-space()='Unlike']"
        )))
        driver.execute_script("arguments[0].click();", unlike_btn)

        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'_a9-z')]//button[.//div[normalize-space()='Unlike']]"
        )))
        driver.execute_script("arguments[0].click();", confirm_btn)

        log(f"✅ Batch {batch_no} done")

        if batch_no < MAX_BATCHES:
            pause = random.uniform(*PROFILE["batch_pause"])
            log(f"⏸️ Waiting {pause:.1f}s")
            time.sleep(pause)
            driver.get(LIKES_URL)
            r_sleep(5, 7)

    log("🎉 ALL DONE")

except Exception:
    log("❌ BOT CRASHED")
    traceback.print_exc()

finally:
    input("\n🟢 Press ENTER to exit (browser stays open)")
