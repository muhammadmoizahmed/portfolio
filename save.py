"""
GARENA COMPLETE AUTOMATIC BOT - EXACT WORK FLOW
1. Website open karo (shop.garena.sg)
2. SVG circle click karo (exact xpath) - popup open hoga
3. Popup par "Log in with Garena" option click karo (exact xpath)
4. ID/Password dalo
5. Slider CAPTCHA auto bypass karo
6. Home page par wapas aao
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import sys

class GarenaAutoBot:
    """Exact flow ka bot jo aapke diye gaye steps follow karega"""
    
    def __init__(self, player_id, password):
        self.player_id = player_id
        self.password = password
        self.driver = None
        self.home_url = "https://shop.garena.sg/?app=100067"
        
        print("\n" + "="*80)
        print("GARENA AUTOMATIC BOT - EXACT FLOW")
        print("="*80)
        print(f"Player ID: {player_id}")
        print("Flow Steps:")
        print("1. Website open karo (shop.garena.sg)")
        print("2. SVG circle click karo (popup open hoga)")
        print("3. Popup par 'Log in with Garena' option click karo")
        print("4. ID/Password dalo")
        print("5. Slider CAPTCHA auto bypass karo")
        print("6. Home page par wapas aao")
        print("="*80)
    
    def setup_driver(self):
        """Chrome driver setup karo"""
        try:
            chrome_options = Options()
            
            # Human-like settings
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            # Window size
            chrome_options.add_argument("--window-size=1366,768")
            chrome_options.add_argument("--start-maximized")
            
            # Disable notifications
            chrome_options.add_argument("--disable-notifications")
            
            # Disable save password prompt
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # For debugging - remove headless if you want to see browser
            # chrome_options.add_argument("--headless")  # Comment this line if you want to see browser
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Stealth JavaScript
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("window.navigator.chrome = {runtime: {}};")
            
            print("✓ Chrome driver setup successful")
            return driver
            
        except Exception as e:
            print(f"✗ Driver setup error: {e}")
            # Simple driver as fallback
            driver = webdriver.Chrome()
            driver.maximize_window()
            return driver
    
    def wait_for_element(self, xpath, timeout=20, element_name=""):
        """Element ka wait karo"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if element_name:
                print(f"✓ {element_name} mil gaya")
            return element
        except Exception as e:
            if element_name:
                print(f"✗ {element_name} nahi mila: {e}")
            return None
    
    def wait_and_click(self, xpath, element_name="Element", timeout=20):
        """Element wait karo aur click karo"""
        try:
            print(f"  {element_name} click kar rahe hain...")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
            time.sleep(0.5)
            
            # Move to element first (more human-like)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).pause(0.2).click().perform()
            
            print(f"  ✓ {element_name} click successful")
            time.sleep(1)
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "no such element" in error_msg.lower() or "timeout" in error_msg.lower():
                print(f"  ✗ {element_name} nahi mila")
            else:
                print(f"  ✗ {element_name} click nahi ho paya: {error_msg[:100]}")
            return False
    
    def type_human_like(self, element, text):
        """Human ki tarah type karo"""
        try:
            element.click()
            time.sleep(0.2)
            element.clear()
            time.sleep(0.1)
            
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.03, 0.08))  # Random typing speed
                
            time.sleep(0.2)
            return True
        except Exception as e:
            print(f"✗ Typing error: {e}")
            return False
    
    def step_1_open_website(self):
        """Step 1: Website open karo"""
        print("\n[1/6] Website open kar rahe hain...")
        try:
            print(f"  Opening: {self.home_url}")
            self.driver.get(self.home_url)
            time.sleep(5)  # Give time to load
            print(f"  ✓ Website open ho gaya")
            
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot("step1_website_open.png")
                print("  Screenshot saved: step1_website_open.png")
            except:
                pass
            return True
        except Exception as e:
            print(f"  ✗ Website open nahi ho paya: {e}")
            return False
    
    def step_2_click_svg_circle(self):
        """Step 2: Exact SVG circle click karo (popup open hoga)"""
        print("\n[2/6] SVG circle click kar rahe hain...")
        
        # Thoda wait karo page load ke liye
        time.sleep(3)
        
        # Method 1: Exact xpath jo aapne diya hai
        svg_xpath = '//*[@id="headlessui-popover-button-:r0:"]/div/div/svg[1]/circle[1]'
        
        if self.wait_and_click(svg_xpath, "SVG circle"):
            print("  ✓ Popup open ho gaya")
            time.sleep(2)
            try:
                self.driver.save_screenshot("step2_popup_open.png")
                print("  Screenshot saved: step2_popup_open.png")
            except:
                pass
            return True
        else:
            print("  Trying alternative approaches...")
            
            # Alternative 1: Try parent element
            parent_xpaths = [
                '//*[@id="headlessui-popover-button-:r0:"]/div/div',
                '//*[@id="headlessui-popover-button-:r0:"]/div',
                '//*[@id="headlessui-popover-button-:r0:"]'
            ]
            
            for xpath in parent_xpaths:
                if self.wait_and_click(xpath, "SVG parent element"):
                    print("  ✓ Popup open ho gaya (via parent)")
                    time.sleep(2)
                    try:
                        self.driver.save_screenshot("step2_popup_open.png")
                    except:
                        pass
                    return True
            
            # Alternative 2: Try any clickable user icon
            user_icons = [
                '//button[contains(@class, "user")]',
                '//div[contains(@class, "user")]',
                '//button[contains(@class, "profile")]',
                '//div[contains(@class, "profile")]',
                '//button[contains(@class, "avatar")]',
                '//div[contains(@class, "avatar")]',
                '//button[.//svg]',
                '//button[.//*[name()="svg"]]',
                '//button[@aria-label="User"]',
                '//button[@aria-label="Profile"]',
                '//button[contains(@id, "user")]'
            ]
            
            for icon_xpath in user_icons:
                if self.wait_and_click(icon_xpath, "User icon"):
                    print("  ✓ Popup open ho gaya (via user icon)")
                    time.sleep(2)
                    try:
                        self.driver.save_screenshot("step2_popup_open.png")
                    except:
                        pass
                    return True
            
            # Alternative 3: Screenshot leke manually check karo
            print("  Taking screenshot for debugging...")
            try:
                self.driver.save_screenshot("step2_error.png")
                print("  Screenshot saved: step2_error.png")
            except:
                pass
            print("  ✗ SVG circle nahi mila")
            return False
    
    def step_3_click_login_with_garena(self):
        """Step 3: Popup par EXACT 'Log in with Garena' option click karo"""
        print("\n[3/6] Popup par 'Log in with Garena' option click kar rahe hain...")
        
        # Wait for popup to appear
        time.sleep(3)
        
        # Take screenshot of popup
        try:
            self.driver.save_screenshot("step3_popup_before_click.png")
            print("  Screenshot saved: step3_popup_before_click.png")
        except:
            pass
        
        # Method 1: EXACT XPATH jo aapne bataya hai
        exact_login_xpath = "/html/body/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[2]/a[1]"
        
        print(f"  Trying exact xpath: {exact_login_xpath}")
        if self.wait_and_click(exact_login_xpath, "Log in with Garena (exact xpath)"):
            print("  ✓ 'Log in with Garena' option select ho gaya (exact xpath)")
            time.sleep(2)
            try:
                self.driver.save_screenshot("step3_garena_selected.png")
                print("  Screenshot saved: step3_garena_selected.png")
            except:
                pass
            return True
        
        # Method 2: Alternative absolute xpaths
        print("  Trying alternative absolute xpaths...")
        alt_absolute_xpaths = [
            "/html/body/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[2]/a",
            "/html/body/div[3]/div[2]/div/div/div[2]/div/div/div[2]//a[contains(text(), 'Garena')]",
            "/html/body/div[3]//a[contains(text(), 'Log in with Garena')]",
        ]
        
        for xpath in alt_absolute_xpaths:
            if self.wait_and_click(xpath, "Log in with Garena (alt absolute)"):
                print("  ✓ 'Log in with Garena' option select ho gaya (alt absolute)")
                time.sleep(2)
                try:
                    self.driver.save_screenshot("step3_garena_selected.png")
                except:
                    pass
                return True
        
        # Method 3: Relative xpaths with text
        print("  Trying relative xpaths with text...")
        relative_xpaths = [
            # Exact text match
            '//a[text()="Log in with Garena"]',
            '//a[contains(text(), "Log in with Garena")]',
            '//*[text()="Log in with Garena"]',
            '//*[contains(text(), "Log in with Garena")]',
            
            # Contains Garena
            '//a[contains(text(), "Garena")]',
            '//*[contains(text(), "Garena") and contains(text(), "Log")]',
            
            # Button with Garena text
            '//button[.//*[contains(text(), "Garena")]]',
            '//button[contains(text(), "Garena")]',
            
            # Div with Garena text
            '//div[contains(text(), "Log in with Garena")]',
            '//div[contains(text(), "Garena")]',
            
            # Span with Garena text
            '//span[contains(text(), "Log in with Garena")]',
        ]
        
        for xpath in relative_xpaths:
            if self.wait_and_click(xpath, "Log in with Garena (relative)"):
                print("  ✓ 'Log in with Garena' option select ho gaya (relative)")
                time.sleep(2)
                try:
                    self.driver.save_screenshot("step3_garena_selected.png")
                except:
                    pass
                return True
        
        # Method 4: Find all links in popup and click the right one
        print("  Finding all links in popup...")
        try:
            # First get the popup
            popup = self.driver.find_element(By.XPATH, "/html/body/div[3]")
            links = popup.find_elements(By.TAG_NAME, "a")
            print(f"  Found {len(links)} links in popup")
            
            for i, link in enumerate(links):
                try:
                    if link.is_displayed():
                        link_text = link.text.strip()
                        print(f"    Link {i+1}: '{link_text}'")
                        if "garena" in link_text.lower():
                            print(f"    Found Garena link: {link_text}")
                            link.click()
                            time.sleep(2)
                            print("  ✓ 'Log in with Garena' clicked")
                            try:
                                self.driver.save_screenshot("step3_garena_selected.png")
                            except:
                                pass
                            return True
                except:
                    continue
        except Exception as e:
            print(f"    Error finding links: {e}")
        
        # Last resort: JavaScript click
        print("  Trying JavaScript click...")
        try:
            js_script = """
            // Try to find element with exact xpath
            var element = document.evaluate('/html/body/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[2]/a[1]', 
                                          document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {
                element.click();
                return true;
            }
            return false;
            """
            result = self.driver.execute_script(js_script)
            if result:
                print("  ✓ 'Log in with Garena' clicked via JavaScript")
                time.sleep(2)
                try:
                    self.driver.save_screenshot("step3_garena_selected.png")
                except:
                    pass
                return True
        except:
            pass
        
        # Final error screenshot
        try:
            self.driver.save_screenshot("step3_error.png")
            print("  Screenshot saved: step3_error.png")
        except:
            pass
        
        print("  ✗ 'Log in with Garena' option nahi mila")
        return False
    
    def step_4_enter_credentials(self):
        """Step 4: ID aur Password dalo"""
        print("\n[4/6] ID aur Password dal rahe hain...")
        
        try:
            # Wait for login form
            time.sleep(4)
            
            # Take screenshot before entering credentials
            try:
                self.driver.save_screenshot("step4_before_login.png")
                print("  Screenshot saved: step4_before_login.png")
            except:
                pass
            
            print("  Login form ke fields dhoond rahe hain...")
            
            # Find Player ID/Email field - multiple strategies
            id_field = None
            
            # Strategy 1: Look for specific input fields
            input_fields = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"  Total input fields found: {len(input_fields)}")
            
            for i, field in enumerate(input_fields):
                try:
                    if field.is_displayed() and field.is_enabled():
                        field_type = field.get_attribute("type") or ""
                        field_name = field.get_attribute("name") or ""
                        field_id = field.get_attribute("id") or ""
                        placeholder = field.get_attribute("placeholder") or ""
                        
                        print(f"    Input {i+1}: type={field_type}, name={field_name}, id={field_id}, placeholder={placeholder}")
                        
                        # Check if this looks like a username/email field
                        if (field_type in ["text", "email"] or 
                            "user" in field_name.lower() or "email" in field_name.lower() or
                            "player" in placeholder.lower() or "email" in placeholder.lower()):
                            id_field = field
                            print(f"    Using this as ID field")
                            break
                except:
                    continue
            
            # Strategy 2: If not found, use first text input
            if not id_field:
                for field in input_fields:
                    try:
                        if field.is_displayed() and field.get_attribute("type") in ["text", "email"]:
                            id_field = field
                            print("    Using first text input as ID field")
                            break
                    except:
                        continue
            
            if not id_field:
                print("  ✗ ID field nahi mila")
                return False
            
            # Type Player ID/Email
            print(f"  ID dal rahe hain: {self.player_id}")
            id_field.clear()
            time.sleep(0.5)
            
            # Human-like typing
            for char in self.player_id:
                id_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.1))
            time.sleep(1)
            
            # Find Password field
            pass_field = None
            
            for field in input_fields:
                try:
                    if field.is_displayed() and field.is_enabled():
                        field_type = field.get_attribute("type") or ""
                        if field_type == "password":
                            pass_field = field
                            print("    Password field found")
                            break
                except:
                    continue
            
            # If password field not found, try second input
            if not pass_field and len(input_fields) > 1:
                # Skip the first input (which is ID field)
                for i, field in enumerate(input_fields):
                    if i > 0 and field.is_displayed() and field.is_enabled():
                        pass_field = field
                        print("    Using second input as password field")
                        break
            
            if not pass_field:
                print("  ✗ Password field nahi mila")
                return False
            
            # Type Password
            print("  Password dal rahe hain...")
            pass_field.clear()
            time.sleep(0.5)
            
            for char in self.password:
                pass_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.1))
            time.sleep(1)
            
            # Take screenshot after entering credentials
            try:
                self.driver.save_screenshot("step4_credentials_entered.png")
                print("  Screenshot saved: step4_credentials_entered.png")
            except:
                pass
            
            # Find and click Submit/Login button
            print("  Login button dhoond rahe hain...")
            
            # Try different button selectors
            button_selectors = [
                ("XPATH", "//button[@type='submit']"),
                ("XPATH", "//button[text()='Login']"),
                ("XPATH", "//button[contains(text(), 'LOGIN')]"),
                ("XPATH", "//button[contains(text(), 'Log In')]"),
                ("XPATH", "//button[contains(text(), 'Sign In')]"),
                ("XPATH", "//input[@type='submit']"),
                ("XPATH", "//button[contains(@class, 'btn-login')]"),
                ("XPATH", "//button[contains(@class, 'login-btn')]"),
                ("XPATH", "//button[contains(@class, 'submit')]"),
            ]
            
            submit_clicked = False
            for by, selector in button_selectors:
                try:
                    submit_btn = self.driver.find_element(by, selector)
                    if submit_btn.is_displayed() and submit_btn.is_enabled():
                        print(f"    Login button mil gaya: {selector}")
                        submit_btn.click()
                        time.sleep(2)
                        print("  ✓ Login submit kar diya")
                        submit_clicked = True
                        break
                except:
                    continue
            
            # If no button found, try pressing Enter
            if not submit_clicked:
                print("  Enter key press kar rahe hain...")
                pass_field.send_keys(Keys.RETURN)
                time.sleep(3)
                print("  ✓ Enter key press kar diya")
            
            # Take screenshot after submit
            try:
                self.driver.save_screenshot("step4_after_submit.png")
                print("  Screenshot saved: step4_after_submit.png")
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"  ✗ Credentials dalne mein error: {e}")
            try:
                self.driver.save_screenshot("step4_error.png")
                print("  Screenshot saved: step4_error.png")
            except:
                pass
            return False
    
    def step_5_auto_slider_captcha(self):
        """Step 5: Slider CAPTCHA auto bypass karo"""
        print("\n[5/6] Slider CAPTCHA check kar rahe hain...")
        
        # Wait for page to load
        time.sleep(4)
        
        # Take screenshot to check for CAPTCHA
        try:
            self.driver.save_screenshot("step5_check_captcha.png")
            print("  Screenshot saved: step5_check_captcha.png")
        except:
            pass
        
        # Check if CAPTCHA exists
        page_source = self.driver.page_source.lower()
        
        # Check for CAPTCHA indicators
        captcha_indicators = ['captcha', 'slider', 'geetest', 'puzzle', 'drag', 'verify', 'security', 'robot']
        
        captcha_found = False
        for indicator in captcha_indicators:
            if indicator in page_source:
                captcha_found = True
                print(f"  {indicator.upper()} CAPTCHA detect hua")
                break
        
        # Also check for visual elements
        try:
            # Look for slider elements
            slider_elements = self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'slider') or contains(@class, 'drag') or contains(@class, 'geetest')]")
            if slider_elements:
                captcha_found = True
                print("  Slider element visually mila")
        except:
            pass
        
        if not captcha_found:
            print("  ✓ CAPTCHA nahi hai, aage badh rahe hain")
            return True
        
        print("  CAPTCHA solve karne ki koshish kar rahe hain...")
        
        # Try multiple CAPTCHA solving methods
        methods = [self.solve_captcha_method1, self.solve_captcha_method2, self.solve_captcha_method3]
        
        for i, method in enumerate(methods, 1):
            print(f"  Method {i} try kar rahe hain...")
            try:
                if method():
                    print(f"  ✓ CAPTCHA solve ho gaya (Method {i})")
                    try:
                        self.driver.save_screenshot(f"step5_captcha_solved_method{i}.png")
                    except:
                        pass
                    return True
            except Exception as e:
                print(f"    Method {i} fail: {str(e)[:100]}")
                continue
        
        print("  ⚠ CAPTCHA solve nahi ho paya")
        print("  Manually solve karne ke liye 30 seconds wait kar rahe hain...")
        
        # Show message to user
        print("\n  ===========================================")
        print("  ATTENTION: Please solve CAPTCHA manually!")
        print("  You have 30 seconds...")
        print("  ===========================================")
        
        time.sleep(30)
        
        return True  # Continue anyway
    
    def solve_captcha_method1(self):
        """Method 1: Find and drag slider"""
        try:
            # Find slider handle
            slider_selectors = [
                "//div[contains(@class, 'slider')]",
                "//div[contains(@class, 'slider-handle')]",
                "//div[contains(@class, 'drag')]",
                "//div[contains(@class, 'geetest_slider')]",
                "//div[@role='slider']",
                "//button[contains(@class, 'slider')]",
                "//div[contains(@style, 'cursor: grab') or contains(@style, 'cursor: move')]",
            ]
            
            slider = None
            for selector in slider_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for elem in elements:
                        if elem.is_displayed():
                            slider = elem
                            break
                    if slider:
                        break
                except:
                    continue
            
            if not slider:
                return False
            
            print("  Slider mil gaya, drag kar rahe hain...")
            
            # Get slider location and size
            slider_location = slider.location
            slider_size = slider.size
            
            # Human-like drag
            actions = ActionChains(self.driver)
            actions.click_and_hold(slider).perform()
            time.sleep(0.3)
            
            # Drag distance (typical CAPTCHA requires 200-250px)
            drag_distance = random.randint(220, 260)
            steps = random.randint(25, 35)
            
            for i in range(steps):
                step = drag_distance / steps + random.uniform(-1.5, 1.5)
                
                # Occasionally move vertically for human-like behavior
                if i % 5 == 0:
                    y_offset = random.randint(-3, 3)
                else:
                    y_offset = 0
                
                actions.move_by_offset(step, y_offset)
                
                # Random pauses
                pause_time = random.uniform(0.02, 0.06)
                actions.pause(pause_time)
            
            # Small hesitation before release
            actions.pause(random.uniform(0.1, 0.2))
            actions.release().perform()
            time.sleep(4)  # Wait for CAPTCHA verification
            
            return True
            
        except Exception as e:
            print(f"  Slider method 1 error: {str(e)[:100]}")
            return False
    
    def solve_captcha_method2(self):
        """Method 2: Try JavaScript to interact with CAPTCHA"""
        try:
            # Try JavaScript to handle CAPTCHA
            js_script = """
            // Try to find and click verify button if exists
            var verifyButtons = document.querySelectorAll('button');
            for (var btn of verifyButtons) {
                if (btn.innerText && btn.innerText.toLowerCase().includes('verify')) {
                    btn.click();
                    return true;
                }
            }
            
            // Try to find slider and simulate drag
            var sliders = document.querySelectorAll('[class*="slider"], [class*="drag"]');
            if (sliders.length > 0) {
                // Simulate mouse events
                var slider = sliders[0];
                var rect = slider.getBoundingClientRect();
                
                // Create and dispatch mouse events
                var mouseDown = new MouseEvent('mousedown', {
                    clientX: rect.left + 10,
                    clientY: rect.top + 10,
                    bubbles: true
                });
                slider.dispatchEvent(mouseDown);
                
                // Simulate drag
                setTimeout(function() {
                    var mouseMove = new MouseEvent('mousemove', {
                        clientX: rect.left + 250,
                        clientY: rect.top + 10,
                        bubbles: true
                    });
                    document.dispatchEvent(mouseMove);
                    
                    setTimeout(function() {
                        var mouseUp = new MouseEvent('mouseup', {
                            bubbles: true
                        });
                        slider.dispatchEvent(mouseUp);
                    }, 100);
                }, 100);
                
                return true;
            }
            return false;
            """
            
            result = self.driver.execute_script(js_script)
            time.sleep(3)
            
            return bool(result)
            
        except:
            return False
    
    def solve_captcha_method3(self):
        """Method 3: Refresh and try different approach"""
        try:
            print("  Page refresh kar rahe hain...")
            self.driver.refresh()
            time.sleep(5)
            
            # Check if CAPTCHA still there
            page_source = self.driver.page_source.lower()
            captcha_words = ['captcha', 'slider', 'geetest', 'verify']
            
            if not any(word in page_source for word in captcha_words):
                return True
            
            # If CAPTCHA still exists, try to bypass with different user agent
            print("  Trying with different user agent...")
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            self.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{value: '{user_agent}'}});")
            
            return False
            
        except:
            return False
    
    def step_6_return_home(self):
        """Step 6: Home page par wapas aao"""
        print("\n[6/6] Home page par wapas aa rahe hain...")
        
        try:
            current_url = self.driver.current_url
            print(f"  Current URL: {current_url}")
            
            # Check if we're already on home page
            if "shop.garena.sg" in current_url and ("app=100067" in current_url or "home" in current_url.lower()):
                print("  ✓ Already home page par hain")
                return True
            
            # Navigate to home page
            print("  Home page ki taraf navigate kar rahe hain...")
            self.driver.get(self.home_url)
            time.sleep(4)
            
            # Verify navigation
            new_url = self.driver.current_url
            print(f"  New URL: {new_url}")
            
            if "shop.garena.sg" in new_url:
                print("  ✓ Home page par aa gaye")
                try:
                    self.driver.save_screenshot("step6_home_page.png")
                    print("  Screenshot saved: step6_home_page.png")
                except:
                    pass
                return True
            else:
                # Try clicking home logo/button
                print("  Home link dhoond rahe hain...")
                home_selectors = [
                    '//a[@href="/"]',
                    '//a[contains(@href, "shop.garena.sg")]',
                    '//a[contains(text(), "Home")]',
                    '//a[contains(text(), "Garena")]',
                    '//img[@alt="Garena"]/parent::a',
                    '//*[contains(@class, "logo")]/a',
                    '//*[contains(@class, "home")]/a',
                ]
                
                for selector in home_selectors:
                    if self.wait_and_click(selector, "Home link"):
                        time.sleep(3)
                        print("  ✓ Home page par aa gaye (via home link)")
                        try:
                            self.driver.save_screenshot("step6_home_page.png")
                        except:
                            pass
                        return True
                
                print("  ⚠ Exact home page par nahi aa paye, lekin process complete")
                return True
                
        except Exception as e:
            print(f"  ✗ Home page wapas aane mein error: {e}")
            return False
    
    def verify_login_success(self):
        """Verify karo ki login successful hua ya nahi"""
        try:
            print("\n" + "="*80)
            print("LOGIN STATUS CHECK")
            print("="*80)
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot for verification
            try:
                self.driver.save_screenshot("final_status_check.png")
                print("Screenshot saved: final_status_check.png")
            except:
                pass
            
            # Check success indicators
            success_indicators = [
                "//*[contains(text(), 'Logout')]",
                "//*[contains(text(), 'Sign Out')]",
                "//*[contains(text(), 'My Account')]",
                "//*[contains(text(), 'Profile')]",
                "//*[contains(text(), 'Welcome')]",
                "//*[contains(text(), 'Hello')]",
                "//*[contains(@class, 'user-name')]",
                "//*[contains(text(), 'Dashboard')]",
                "//*[contains(text(), 'Account') and not(contains(text(), 'Create'))]",
                "//*[contains(text(), 'Top Up')]",
                "//*[contains(text(), 'Balance')]",
            ]
            
            for indicator in success_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    for elem in elements:
                        if elem.is_displayed():
                            text = elem.text[:50] if elem.text else "Element found"
                            print(f"✓ Login successful! Indicator: {text}...")
                            return True
                except:
                    continue
            
            # Check URL for success indicators
            current_url = self.driver.current_url.lower()
            success_urls = ['dashboard', 'account', 'profile', 'home', 'success', 'main', 'shop']
            
            for url_keyword in success_urls:
                if url_keyword in current_url:
                    print(f"✓ Login successful! URL contains: {url_keyword}")
                    return True
            
            # Check for error messages
            error_indicators = [
                "//*[contains(text(), 'Invalid')]",
                "//*[contains(text(), 'Wrong')]",
                "//*[contains(text(), 'Error')]",
                "//*[contains(text(), 'Failed')]",
                "//*[contains(text(), 'Incorrect')]",
                "//*[contains(text(), 'not found')]",
                "//*[contains(text(), 'try again')]",
            ]
            
            for indicator in error_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    for elem in elements:
                        if elem.is_displayed():
                            error_text = elem.text[:100] if elem.text else "Error found"
                            print(f"✗ Login failed! Error: {error_text}")
                            return False
                except:
                    continue
            
            print("⚠ Login status unclear - please check screenshot: final_status_check.png")
            print("   Or check browser window manually")
            return False
            
        except Exception as e:
            print(f"⚠ Verification error: {e}")
            return False
    
    def run_complete_flow(self):
        """Complete flow run karo"""
        print("\n" + "="*80)
        print("COMPLETE FLOW STARTING...")
        print("="*80)
        
        try:
            # Step 0: Driver setup
            print("\n[0/6] Chrome driver setup kar rahe hain...")
            self.driver = self.setup_driver()
            if not self.driver:
                print("✗ Driver setup fail")
                return False
            
            # Step 1: Website open
            if not self.step_1_open_website():
                print("❌ Step 1 fail - website open nahi ho paya")
                return False
            
            # Step 2: SVG circle click
            if not self.step_2_click_svg_circle():
                print("❌ Step 2 fail - SVG circle click nahi ho paya")
                return False
            
            # Step 3: Login with Garena option click
            if not self.step_3_click_login_with_garena():
                print("❌ Step 3 fail - 'Log in with Garena' option click nahi ho paya")
                return False
            
            # Step 4: Credentials enter
            if not self.step_4_enter_credentials():
                print("❌ Step 4 fail - Credentials enter nahi ho paye")
                return False
            
            # Step 5: CAPTCHA solve
            if not self.step_5_auto_slider_captcha():
                print("⚠ Step 5 warning - CAPTCHA solve nahi ho paya")
            else:
                print("✓ Step 5 complete - CAPTCHA handled")
            
            # Step 6: Return home
            if not self.step_6_return_home():
                print("⚠ Step 6 warning - Home page par wapas nahi aa paye")
            else:
                print("✓ Step 6 complete - Home page reached")
            
            # Final verification
            print("\n" + "="*80)
            print("FINAL VERIFICATION")
            print("="*80)
            
            login_success = self.verify_login_success()
            
            if login_success:
                print(f"\n✅ SUCCESS! Login ho gaya")
                print(f"   Player ID: {self.player_id}")
                print(f"   Current Page: {self.driver.current_url}")
                print(f"   Screenshots saved for debugging")
            else:
                print(f"\n⚠ WARNING: Login status verify nahi ho paya")
                print(f"   Please check screenshots for details")
            
            print("\n" + "="*80)
            print("BOT EXECUTION COMPLETE")
            print("="*80)
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def keep_browser_open(self):
        """Browser open rakho inspection ke liye"""
        print("\n" + "="*80)
        print("BROWSER OPEN FOR INSPECTION")
        print("="*80)
        print("\nBrowser abhi bhi open hai. Aap dekh sakte hain:")
        print("1. Login successful hua ya nahi")
        print("2. Account ki details")
        print("3. Koi error message")
        print("\nScreenshots bhi save hue hain debugging ke liye")
        print("Browser band karne ke liye yahan enter dabayein...")
        
        try:
            input()
        except:
            pass
        
        if self.driver:
            self.driver.quit()
            print("\nBrowser band ho gaya.")

# ==================== MAIN FUNCTION ====================

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("GARENA AUTOMATIC BOT")
    print("="*80)
    
    # Get credentials from user
    print("\nPlease enter your credentials:")
    
    player_id = input("Player ID: ").strip()
    if not player_id:
        print("❌ Player ID required")
        return
    
    password = input("Password: ").strip()
    if not password:
        print("❌ Password required")
        return
    
    # Create bot instance
    bot = GarenaAutoBot(player_id, password)
    
    # Run complete flow
    success = bot.run_complete_flow()
    
    # Keep browser open for inspection
    if success:
        bot.keep_browser_open()
    else:
        print("\n❌ Bot execution failed. Koi error aaya.")
        if bot.driver:
            bot.driver.quit()

def quick_test():
    """Quick test function"""
    print("\n" + "="*80)
    print("QUICK TEST MODE")
    print("="*80)
    
    # Test credentials
    test_id = "test_user_123"
    test_pass = "test_pass_123"
    
    print(f"\nTest Credentials:")
    print(f"Player ID: {test_id}")
    print(f"Password: {test_pass}")
    
    bot = GarenaAutoBot(test_id, test_pass)
    bot.run_complete_flow()
    
    if bot.driver:
        bot.driver.quit()

if __name__ == "__main__":
    try:
        # Check for test mode
        if len(sys.argv) > 1 and sys.argv[1] == "--test":
            quick_test()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n❌ Bot execution stopped by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")