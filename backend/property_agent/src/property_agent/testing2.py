import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    DomainFilter,
    URLPatternFilter,
    ContentTypeFilter
)
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import time
import datetime
import json
import re
import html
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_region_links(driver):
    element = driver.find_elements(By.CSS_SELECTOR, 'a.headerRegionLink')
    return element

def get_project_links(url):

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new") 
    options.add_argument("window-size=1920,1080")

    driver = webdriver.Firefox(options=options)
    driver.get(url)

    property_menu = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(., 'Property') and contains(@class, 'dropdown-toggle')]")
    ))

    # Click using JS to avoid hover-only interaction
    driver.execute_script("arguments[0].click();", property_menu)

    time.sleep(1.5)

    # Get all region links
    region_links = WebDriverWait(driver, 15).until(get_region_links)

    all_project_urls = []
    
    # Process each region link dynamically
    for region_link in region_links:
        region_name = region_link.text.strip()
        region_type = region_link.get_attribute("data-type")
        
        print(f"Processing region: {region_name} ({region_type})")

        # Click region using JS to trigger the page’s native JS
        driver.execute_script("arguments[0].click();", region_link)

        # Wait for content to load — we assume some project cards will appear
        time.sleep(10)

        #load more
        # load_more = driver.find_elements(By.CSS_SELECTOR, '#loadMore')
        # driver.execute_script("arguments[0].click();", load_more)
        # time.sleep(1.5)

        # Find all project cards now visible (inside the region projects container)
        project_links = driver.find_elements(By.CSS_SELECTOR, '.region-projects .tab-pane.active a.s-card')
        
        for link in project_links:
            url = link.get_attribute("href")
            if url not in all_project_urls:
                print(f"  → Found project: {url}")
                all_project_urls.append(url)

    # print(all_project_urls)
    print("Property found:")
    for project in all_project_urls:
        print(project)
    print(f"\nTotal projects found: {len(all_project_urls)}")
    driver.quit()

    return all_project_urls

def save_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name.strip().lower())[:80]

# To fix broken html
def fix_data_product_attr(html_string, attr_names=["data-product", "data-ga-details"]):
    for attr_name in attr_names:
        # Dynamically create regex pattern for each attribute
        pattern = rf'{attr_name}="({{.*?}})"'

        def escape_json_quotes(match):
            json_str = match.group(1)
            escaped_json = json_str.replace('"', '&quot;')
            return f'{attr_name}="{escaped_json}"'

        html_string = re.sub(pattern, escape_json_quotes, html_string)
    return html_string

def extract_format_data(result):
    decoded_html = html.unescape(result.html)
    fixed_html = fix_data_product_attr(decoded_html)
    soup = BeautifulSoup(fixed_html, "html5lib")

    # === Property Name
    a_tag = soup.find('a', class_='gaTracking', attrs={'data-ga-details': True})
    if a_tag and a_tag.has_attr('data-ga-details'):
        data_ga_details = html.unescape(a_tag['data-ga-details'])
        data = json.loads(data_ga_details)
        property_name = data.get("property_name")
    else:
        property_name = "N/A"

    # === Location
    location_tag = soup.title.string if soup.title else ""
    location = location_tag.split('|')[0].strip()

    # === Description
    section = soup.find("div", class_="secgeneral-pad wyaxis txtsgeneral")
    description_tag = section.find("p") if section else None
    description = description_tag.get_text(separator=' ', strip=True) if description_tag else "N/A"

    # === Showroom
    details = soup.select('.row.cproperty-showcase-details')
    showroom_info = {}

    for detail in details:
        label_tag = detail.select_one('.cproperty-showcase-details-left')
        value_tag = detail.select_one('.cproperty-showcase-details-right')
        
        if label_tag and value_tag:
            label = label_tag.get_text(strip=True).lower()
            raw_value = " ".join(value_tag.stripped_strings)
            value = re.sub(r'\s+', ' ', raw_value).strip() if raw_value else ""

            if 'address' in label:
                showroom_info['address'] = value
            elif 'operating' in label:
                showroom_info['operating_hours'] = value
            elif 'hotline' in label:
                # Get the phone number from the <a> tag if available
                phone = value_tag.select_one('a')
                showroom_info['hotline'] = phone.get_text(strip=True) if phone else value

    # === Bedrooms
    bedrooms_tag = soup.select_one(".icouems-bedrooms + div .text")
    bedrooms = bedrooms_tag.get_text(strip=True).split()[0] if bedrooms_tag else "N/A"

    # === Bathrooms
    bathrooms_tag = soup.select_one(".icouems-bathrooms + div .text")
    bathrooms = bathrooms_tag.get_text(strip=True).split()[0] if bathrooms_tag else "N/A"

    # === Parking Lots
    parking_tag = soup.select_one(".icouems-parkings + div .text")
    parking_lots = parking_tag.get_text(strip=True).split()[0] if parking_tag else "N/A"

    # === Built-up Size
    built_tag = soup.find("div", string=lambda s: s and "Built-up" in s)
    built_up_size = built_tag.find_next_sibling("div").get_text(strip=True) if built_tag else "N/A"

    # === Price
    price_tag = soup.select_one("#propertyPrice")
    price = " ".join(price_tag.stripped_strings) if price_tag else "N/A"

    # === Status
    status_tag = soup.select_one("#propertyStatus")
    status = status_tag.get_text(strip=True) if status_tag else "N/A"

    # === Tenure
    tenure_tag = soup.find("div", string=lambda s: s and "tenure" in s.lower())
    tenure = tenure_tag.find_next_sibling("div").get_text(strip=True) if tenure_tag else "N/A"

    # === Property Type
    property_type = "N/A"
    labels = soup.find_all("div", class_="col-auto content-cover-detailstxt")
    for label in labels:
        label_text_raw = label.get_text(strip=True)
        label_text = re.sub(r'\s+', ' ', label_text_raw).strip().lower()
        if "property type" in label_text:
            value_div = label.find_next_sibling("div", class_="col content-cover-detailstxt2")
            property_type = value_div.get_text(strip=True) if value_div else "N/A"
            break

    # === Features
    features = [tag.get_text(strip=True) for tag in soup.select(".features-items h3")]
    if not features:
        features = [tag.get_text(strip=True) for tag in soup.select(".features li")]

    # === Nearby Amenities
    nearby_amenities = []
    amenities_blocks = soup.select(".plocations-amenities-icons-text")
    for block in amenities_blocks:
        distance_tag = block.find("div", class_="distance")
        distance = distance_tag.get_text(strip=True) if distance_tag else None
        if distance_tag:
            distance_tag.extract()
        name = block.get_text(strip=True)
        nearby_amenities.append({
            "name": name,
            "distance": distance
        })

    # === Unit Types
    unit_types = []
    options = soup.select("#product-options option")
    for option in options:
        data_product = option.get("data-product")
        if data_product:
            attrs = json.loads(data_product)
            unit = {
                "type": option.text.strip().replace("Type ", ""),
                "bedrooms": attrs.get("bedrooms", 0),
                "bathrooms": attrs.get("bathrooms", 0),
                "parking_lots": attrs.get("parking_spaces", 0),
                "built_up_size": f'{attrs.get("floor_area_from", "N/A")} {(attrs.get("floor_area_unit").strip() if attrs.get("floor_area_from") and attrs.get("floor_area_unit") else "sqft")}',
                "price": f'RM {int(float(attrs.get("price", 0))):,}' if attrs.get("price") else "N/A"
            }
            unit_types.append(unit)

    # === Property Info Structure
    property_info = {
        "property_name": property_name,
        "location": location,
        "showroom": showroom_info,
        "description": description,
        "status": status,
        "tenure": tenure,
        "property_type": property_type,
        "features": features,
        "nearby_amenities": nearby_amenities,
        "unit_types": unit_types,
        "property_offering_details": {
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "parking_lots": parking_lots,
            "built_up_size": built_up_size,
            "price": price
        },
        "url": result.url
    }

    # === Save to File
    file_name = save_filename(property_name if property_name != "N/A" else urlparse(result.url).path)
    file_path = os.path.join("property_json", f"{file_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(property_info, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {file_path}")
    
async def crawl(url="https://www.uemsunrise.com"):
    start = time.process_time()
    # Execute the crawl
    project_links = get_project_links(url)
    #project_links = [ r for r in project_links if 'malaysia-vision-valley' in r]
    results = []
    crawled_urls = []
    
    browser_config = BrowserConfig(
        headless=True,
        browser_type="chromium",
        # viewport_width=1920,
        # viewport_height=1080,
        verbose=True,
        user_agent_mode='random',
        text_mode=True,
    )

    # Create a sophisticated filter chain
    filter_chain = FilterChain([
        # URL patterns to include
        URLPatternFilter(patterns=["*property/region/*"], reverse=False),
        URLPatternFilter(patterns=["*#*"]+crawled_urls, reverse=True),

        # Content type filtering
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    # Create a relevance scorer
    keyword_scorer = KeywordRelevanceScorer(
        keywords=[ "project", "development","region"],
        weight=0.7
    )   

    # Set up the configuration
    config = CrawlerRunConfig(
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=1,
            include_external=False,
            filter_chain=filter_chain,
            url_scorer=keyword_scorer
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        stream=True,
        verbose=True,
        scan_full_page=False,
        # js_code=js_commands,
        # js_only=True,
        wait_for="""
            (() => {
                const propertyTab = Array.from(document.querySelectorAll('p.text-pink.gaTracking')).find(link => link.textContent.includes('Load All Projects'));
                if (propertyTab) {
                    propertyTab.click();
                }
                return true;
            })();
            """,
        # session_id='session',
        page_timeout=100000,
    ) 
     
    # Create a folder to save individual JSON files
    os.makedirs("property_json", exist_ok=True)

    async with AsyncWebCrawler() as crawler:
        for url in project_links:
            print(f"\n Crawling: {url}")

            async for result in await crawler.arun(url, config=config):
                results.append(result)
                crawled_urls.append(result.url)
                score = result.metadata.get("score", 0)
                depth = result.metadata.get("depth", 0)
                print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")
                
                if depth != 0:
                    extract_format_data(result)

    # Analyze the results
    print(f"Crawled {len(results)} high-value pages")
    print(f"Average score: {sum(r.metadata.get('score', 0) for r in results) / len(results):.2f}")

    # Group by depth
    depth_counts = {}
    for result in results:
        depth = result.metadata.get("depth", 0)
        depth_counts[depth] = depth_counts.get(depth, 0) + 1

    print("Pages crawled by depth:")
    for depth, count in sorted(depth_counts.items()):
        print(f"  Depth {depth}: {count} pages")

    print("Crawled page")
    # crawled_urls = sorted(list(set([r.url for r in results])))
    for cu in crawled_urls:
        print("- ", cu)

    print(f"total uniqued crawled page - {len(crawled_urls)}")
    end = time.process_time()
    print("Time taken to run - ",str(datetime.timedelta(seconds=end-start)))
if __name__ == "__main__":
    asyncio.run(crawl())